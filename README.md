# ROS turtle catch up
**Необходимо:** реализовать в ROS программу, которая будет создавать двух черепах, одна из которых будет уплавляться с клавиатуры, а вторая будет преследовать первую.
#### Архитектура
Для запуска нескольких нод одной командой был реализован .launch файл. Данный файл запускает ноды turtlesim_node, turtle_teleop_key, spawner, catcher в указанном порядке.
#### ```spawner.py```
Данный скрипт отвечает за создание второй черепахи через сервис.
```
#! /usr/bin/python
import rospy
from turtlesim.srv import Spawn
rospy.init_node('turtle_spawner')
rospy.wait_for_service('/spawn')
spawner = rospy.ServiceProxy('/spawn', Spawn)
spawner(4.0, 4.0, 4.0, rospy.get_param('~spawned_name'))
```

#### ```catchup.py```
Данный скрипт создает ноду с двумя подписчиками и одним паблишером. Нода отслеживает изменения положения первой черепахи через топик /turtle1/pose, рассчитывает перемещение для ворой черепахи и публикует сообщение в топик /(~spawned_name)/cmd_vel. Второй подписчик обновляет положение второй черепахи. 
```
#! /usr/bin/python
import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class catchuper:
    def __init__(self):
        self.pose = Pose()
        self.pub = rospy.Publisher(str(rospy.get_param('~spawned_name'))+'/cmd_vel', Twist, queue_size=1)
        self.sub1 = rospy.Subscriber('turtle1/pose', Pose, self.catch_up)
        self.sub2 = rospy.Subscriber(str(rospy.get_param('~spawned_name'))+'/pose', Pose, self.refresh_pose)

    def catch_up(self, turtlePos):
        msg = Twist()
        rotate = math.atan2(turtlePos.y - self.pose.y, turtlePos.x - self.pose.x)
        msg.angular.z = rotate - self.pose.theta
	    msg.linear.x = turtlePos.linear_velocity
        self.pub.publish(msg)

    def refresh_pose(self, turtlePos):
        self.pose = turtlePos

rospy.init_node('turtle_catchuper')
catchuper = catchuper()
rospy.spin()
```
#### ```spawner.launch```
Файл для запуска комплекса нод одной командой
```
<launch>
    <arg name="spawned_name" default="donatello"/>
    
    <node name="turtlesim_node" pkg="turtlesim" type="turtlesim_node"/>
    
    <node name="turtle_teleop_key" pkg="turtlesim" type="turtle_teleop_key"/>
    
    <node name="turtle_spawner" pkg="turtle_catch_up" type="spawn.py">
        <param name="spawned_name" value="$(arg spawned_name)" type="string"/>
    </node>

    <node name="turtle_catchuper" pkg="turtle_catch_up" type="catchup.py">
        <param name="spawned_name" value="$(arg spawned_name)" type="string"/>
    </node>
</launch>
```
#### Результаты
Результат работы:
**Гифка сильно зависает, необходимо смотреть около 2 минут, чтобы увидеть весь процесс**
![](https://github.com/Criptonite/ROS/blob/main/lab1/src/turtle_catch_up/images/turtle_catcher.gif)
