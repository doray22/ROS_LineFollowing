#!/usr/bin/env python

#imports ROS libraries and messages
import rospy 
from sensor_msgs.msg import Image
from std_msgs.msg import Int16

#import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node('process_image') #initialize ROS node named 'process_image'
bridge = CvBridge() #initializes CvBridge class

def show_image(img): #function to display cv2 image in a window
	cv2.imshow("Image Window", img)
	cv2.waitKey(3)

def modify(img): #modifies the image(crop + bw)
	height, width, channels = img.shape #height = 800 pixels width = 800
	rows_upper_slice = height - 200
	rows_lower_slice = height
	cols_left_slice = 0
	cols_right_slice = width

	#crop frame and change to a binary image
	cropped = img[rows_upper_slice:rows_lower_slice,cols_left_slice:cols_right_slice]
	gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
  	blur = cv2.GaussianBlur(gray,(9,9),0)
  	ret,bw_frame = cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV)

  	return bw_frame

def bright_point(img):
 	M = cv2.moments(img)
	if (M["m00"] != 0):
		cX = float(M["m10"] / M["m00"])
		return cX
	else:
		return None

def image_callback(img_msg):
	try:
		cv_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
	except CvBridgeError, e:
		rospy.logerr("CvBridge Error: {0}".format(e))
	pub = rospy.Publisher('bright_point', Int16)
	pub.publish(bright_point(modify(cv_image)))

sub_image = rospy.Subscriber('/rrbot/camera1/image_raw', Image, image_callback) #initializes subscriber to "image_raw" topic (which i think was defined in the camera gazebo plugin)

while not rospy.is_shutdown(): #loop that prevents program from shutting down
	rospy.spin()
