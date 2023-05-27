#!/usr/bin/env python3 
import rospy
import serial
import time

stm = serial.Serial(
port = '/dev/ttyUSB1',
baudrate = 9600,
timeout = 5)


if __name__ == '__main__':
    rospy.init_node("serial")

    rospy.logwarn("WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^_^ şaka eheh")
    rospy.loginfo("infosfor")

while  True:
	try:
		stm.write("1".encode())
		time.sleep(2)
		stm.write("0".encode())
		time.sleep(2)

	except Exception as e:
		print(e)
		stm.close()
	pass