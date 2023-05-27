#!/bin/bash

cmd1=rmk
cmd='sudo cd /home/jetson/grad_project_jetson/catkin_ws'
cmd2='roscore'
webcamcmd='rosrun vision webcam_pub_vision.py'
reccmd='rosrun vision recognition.py'
lidarc1='ls -la /dev | grep ttyUSB'
lidarc2='sudo chmod 0666 /dev/ttyUSB0'
lidarc3='roslaunch rplidar_ros view_rplidar.launch'
lidarcslam='roslaunch rplidar_ros rplidar.launch'
tcpcmd='rosrun vision TCP_client.py'
movcmd='rosrun movement movement'
slamcmd='roslaunch hector_slam_launch tutorial.launch'



choice=$1

echo "argumant 1 is $1"

gnome-terminal --command="bash -c '$cmd2; $SHELL'" 

cd /home/jetson/grad_project_jetson/catkin_ws/src/vision/src/imagesCV
rm -rf *

sleep 5

if [ "$1" == "all" ];then #this part runs all the nodes.
	echo "all is running"
	gnome-terminal --command="bash -c '$webcamcmd; $SHELL'" 
	sleep 8
	gnome-terminal --command="bash -c '$reccmd; $SHELL'"
	sleep 70
	gnome-terminal --command="bash -c '$lidarc1; $lidarc2; $lidarc3; $SHELL'"
	sleep 50

elif [ "$1" == "vision" ];then #this part runs only the face recognition.
	echo "vision part is running"
	echo "tcp part is running"
	gnome-terminal --command="bash -c '$tcpcmd; $SHELL'" 
	sleep 10
	gnome-terminal --command="bash -c '$webcamcmd; $SHELL'" 
	sleep 8
	gnome-terminal --command="bash -c '$reccmd; $SHELL'"
	sleep 70


elif [ "$1" == "tcp" ];then 
	echo "tcp part is running"
	gnome-terminal --command="bash -c '$tcpcmd; $SHELL'" 
	sleep 8

elif [ "$1" == "lidar" ];then #this part runs all the nodes.
	echo "lidar is running"
	gnome-terminal --command="bash -c '$lidarc1; $lidarc2; $lidarc3; $SHELL'"
	sleep 15
	gnome-terminal --command="bash -c '$movcmd; $SHELL'" 
	sleep 5

elif [ "$1" == "slam" ];then #this part runs all the nodes.
	echo "slam is running"
	gnome-terminal --command="bash -c '$lidarc1; $lidarc2; $lidarcslam; $SHELL'"
	sleep 15
	gnome-terminal --command="bash -c '$movcmd; $SHELL'" 
	sleep 5
	gnome-terminal --command="bash -c '$slamcmd; $SHELL'"
	sleep 15
#elif [[$1 -eq "tcp_test"]]
#then



else
	echo "Invalid arguments"

fi




rmk (){
	cd /home/jetson/grad_project_jetson/catkin_ws
	catkin_make
	. /home/jetson/grad_project_jetson/catkin_ws/devel/setup.bash
	
}

