#!/usr/bin/env python3 
from recognition import FaceRecognition
import rospy
# pip install cmake dlib==19.22

if __name__ == '__main__':
    rospy.init_node("vision" )
    rospy.loginfo("WASSUP BTCHES")
    fr = FaceRecognition()
    fr.run_recognition()



