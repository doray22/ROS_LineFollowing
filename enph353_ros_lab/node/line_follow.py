#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

rospy.init_node('line_follow')
prev_error = 200

def error(target):
	center = 400
	global prev_error
	if (target.data != 0):
		err = center - target.data
		prev_error = err
	else:
		err = prev_error * 5 #multpilied with a correction factor for sharper turns to find line again
	return err
	
def move_robot(error): #line following algoritms
	p = 100 #correction factor
	pub = rospy.Publisher('/cmd_vel',Twist,queue_size = 1)
	rate = rospy.Rate(2)
	move = Twist()
	move.linear.x = 0.3
	move.angular.z = error / p
	pub.publish(move) #publishes to the skid steering topic

def callback(target):
	move_robot(error(target))
sub_target = rospy.Subscriber('bright_point', Int16, callback) #subscribing to converted_image topid\c

while not rospy.is_shutdown(): #loop that prevents program from shutting down
	rospy.spin()

