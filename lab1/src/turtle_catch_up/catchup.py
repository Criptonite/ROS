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
