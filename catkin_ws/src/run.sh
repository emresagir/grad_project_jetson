#!/bin/bash

cmd1=rmk
cmd='sudo cd /home/jetson/grad_project_jetson/catkin_ws'
cmd2='roscore'
webcamcmd='rosrun vision webcam_pub_vision.py'
reccmd='rosrun vision recognition.py'


choice=$1

echo "argumant 1 is $1"

gnome-terminal --command="bash -c '$cmd2; $SHELL'" 
sleep 5

if [ "$1" == "vision" ];then #this part runs only the face recognition.
	echo "vision part is running"
	gnome-terminal --command="bash -c '$webcamcmd; $SHELL'" 
	sleep 8
	gnome-terminal --command="bash -c '$reccmd; $SHELL'"
	sleep 50
	


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

