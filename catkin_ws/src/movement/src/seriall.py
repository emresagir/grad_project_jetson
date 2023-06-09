#!/usr/bin/env python3 
import rospy
import serial
import time
from std_msgs.msg import String

stm = serial.Serial(
port = '/dev/ttyUSB1',
baudrate = 9600,
timeout = 5)



def callback(data):
		print(data)

		stm.write(data.encode())

if __name__ == '__main__':
    rospy.init_node("serial")

    rospy.logwarn("WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^_^ şaka eheh")
    rospy.loginfo("infosfor")

    rospy.Subscriber("movcmd", String, callback)

    rospy.spin()



		
		


