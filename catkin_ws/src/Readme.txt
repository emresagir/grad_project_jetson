When connect via usb, follow these steps;

################################################
# list USB device and verify permissions
ls -la /dev | grep ttyUSB

# change permissions
sudo chmod 0666 /dev/ttyUSB0

################################################


############# run UI ########################
roslaunch rplidar_ros view_rplidar.launch


#########  sadece rplidar core ###########
roslaunch rplidar_ros rplidar.launch 





##########	Lidar Tutorial     #############
https://softwaretester.info/rplidar-a1-with-ros-melodic-on-ubuntu-18-04/




#########   Lidar hakkındaki bilgiler #############
Çıkıntılı noktası öne bakacak şekilde durduğunda, sol taraf +90 derece, sağ taraf -90 derece.

uzunluk değeri olarak 0.56 = ~56cmye denk gelmekte. minimum ise 10-11cm yakınlığı ölçebilmekte.




##################    For camera on jetson        ####################
https://github.com/JetsonHacksNano/CSI-Camera




#################	For hector slam followed this tutorial #########################
https://automaticaddison.com/how-to-build-an-indoor-map-using-ros-and-lidar-based-slam/





TODO:
SLAMden alınan haritayı kaydetmeye bak 
bu kayıt edilen görüntüyü server'a at
scripte slam'i de ekle
hareket algoritmasını hallet

