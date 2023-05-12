When connect via usb, follow these steps;

################################################

# list USB device and verify permissions
ls -la /dev | grep ttyUSB

# change permissions
sudo chmod 0666 /dev/ttyUSB0


################################################


############# run UI ########################

roslaunch rplidar_ros view_rplidar.launch

#############################################

##########https://softwaretester.info/rplidar-a1-with-ros-melodic-on-ubuntu-18-04/#############

Çıkıntılı noktası öne bakacak şekilde durduğunda, sol taraf +90 derece, sağ taraf -90 derece.

uzunluk değeri olarak 0.56 = ~56cmye denk gelmekte. minimum ise 10-11cm yakınlığı ölçebilmekte.




##################    For camera on jetson        ####################
https://github.com/JetsonHacksNano/CSI-Camera

