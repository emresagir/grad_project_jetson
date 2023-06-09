/*
 * Copyright (c) 2014, RoboPeak
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, 
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, 
 *    this list of conditions and the following disclaimer in the documentation 
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
/*
 *  RoboPeak LIDAR System
 *  RPlidar ROS Node client test app
 *
 *  Copyright 2009 - 2014 RoboPeak Team
 *  http://www.robopeak.com
 * 
 */


#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include "std_msgs/String.h"
#include <sstream>

#define RAD2DEG(x) ((x)*180./M_PI)

bool flag = false;
int left_counter = 0;
ros::Publisher mov_pub;

void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan)
{

    int count = scan->scan_time / scan->time_increment;
    ROS_INFO("I heard a laser scan %s[%d]:", scan->header.frame_id.c_str(), count);
    ROS_INFO("angle_range, %f, %f", RAD2DEG(scan->angle_min), RAD2DEG(scan->angle_max));
  
    for(int i = 0; i < count; i++) {
        float degree = RAD2DEG(scan->angle_min + scan->angle_increment * i);
        
        if(scan->ranges[i] <1000){

            /*
            if(degree == 0){
                std_msgs::String msg;
                std::stringstream ss;
                ss << '&' << (int)(100*scan->ranges[i]) << '&';
                msg.data = ss.str();
                mov_pub.publish(msg);
            }


            if(degree > 90 && degree < 90.3){
                std_msgs::String msg;
                std::stringstream ss;
                ss << '-' << (int)(100*scan->ranges[i]) << '-'; 
                msg.data = ss.str();
                mov_pub.publish(msg);
            }
            */ //commented out for test purposes

            if(degree > -90.3 && degree < -90){
                std_msgs::String msg;
                std::stringstream ss;
                
                if((scan->ranges[i]*100) < 100){
                    
                    ss << '#' << '0' << (int)(100*scan->ranges[i]) << '#';
                }
                else{
                    
                    ss << '#' << (int)(100*scan->ranges[i]) << '#';
                }
                
                msg.data = ss.str();
                mov_pub.publish(msg);
            }
            
        }   


        /*
        //ROS_INFO(": [%f, %f]", degree, scan->ranges[i]);
        left_counter++;
        if (degree > 105 && degree < 110){ // sol arkasında kalmalı duvar, ondan dolayı 85,95 aralığı olmuyor.
            if (scan->ranges[i] > 0.3){
                ROS_INFO(" SOLA DONUS YAP!");
                
                
                if (flag == false){

                    std_msgs::String msg;
                    std::stringstream ss;
                    ss << "sol"; 
                    msg.data = ss.str();
                    mov_pub.publish(msg);
                    flag = true;
                }
                
                else if (flag == true){

                    
                    if (left_counter > 40000){ //fitre 
                        flag = false;
                        left_counter =0;
                    }
                }
                

                
            }            
        }

        if (degree < -85 && degree > -95){
            if(scan->ranges[i] > 0.3){
                //ROS_INFO("SAĞA DÖNÜŞ YAP!");
            }
        }
        //TODO: 
        //filtre eklenecek
        //Önceki değerden fazla çıktığı için uzaklık değeri boşluk bu şekilde anlaşılacak.
        */

    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "rplidar_node_client");
    ros::NodeHandle n;

    mov_pub = n.advertise<std_msgs::String>("movcmd", 1000);
    ros::Subscriber sub = n.subscribe<sensor_msgs::LaserScan>("/scan", 1000, scanCallback);


    ros::spin();

    return 0;
}
