#!/usr/bin/env python3 
import rospy
import serial
import time
import os
from PIL import Image
from std_msgs.msg import String
#/home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesMap
cmd1="cd /home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesMap && rosrun map_server map_saver -f my_map"
cmd2="cd /home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesMap && convert my_map.pgm my_map.png "
if __name__ == '__main__':
	rospy.init_node("savmap")

	rospy.logwarn("WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^_^ şaka eheh")
	rospy.loginfo("infosfor")
	time.sleep(20)

	while True:
		os.system(cmd1)
		time.sleep(1)
		os.system(cmd2)

		im = Image.open(r"/home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesMap/my_map.png")

		# Size of the image in pixels (size of original image)
		# (This is not mandatory)
		width, height = im.size
		 
		# Setting the points for cropped image
		left = (width/2 - 100)
		top = (height/2 - 100)
		right = (width/2 + 100)
		bottom = (height/2 + 100)
		 
		# Cropped image of above dimension
		# (It will not change original image)
		im1 = im.crop((left, top, right, bottom))
		 
		# Shows the image in image viewer
		im1.save("/home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesMap/map.jpg")
		#Save location'ı değiştir.


		time.sleep(10)


	