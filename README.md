# AI-Based Maze Solver Robot

An autonomous robot developed for navigating unknown environments using AI, image processing, and SLAM. The project was designed as a senior Electrical and Electronics Engineering graduation project at Gazi University.

## Features

- Autonomous maze exploration
- Real-time SLAM mapping using Hector SLAM
- Face recognition
- Safe and dangerous area detection
- LIDAR-based navigation
- TCP communication between robot and user interface
- STM32-based motor control with PID
- ROS Noetic based software architecture

## Technologies

- Ubuntu 20.04
- ROS Noetic
- C++
- Python
- OpenCV
- Dlib / face_recognition
- Hector SLAM
- RPLidar
- STM32
- Jetson Nano

## Project Structure

```
catkin_ws/
├── src/
│   ├── movement/
│   ├── serial/
│   ├── image_processing/
│   ├── tcp_client/
│   ├── cv_basics/
│   ├── rplidar_ros/
│   └── hector_slam/
```

## System Overview

The robot operates as a collection of ROS nodes:

- **Movement** – Autonomous navigation algorithm
- **Serial** – Communication with STM32 motor controller
- **Image Processing** – Face recognition and safe/dangerous area detection
- **TCP Client** – Communication with the remote server
- **RP Lidar** – Laser scan acquisition
- **Hector SLAM** – Real-time map generation

The generated map and detected images are transmitted to a remote GUI through a cloud-based TCP server.

## Hardware

- NVIDIA Jetson Nano
- STM32G030 Microcontroller
- RPLidar
- USB Camera
- DC Motors with Encoders
- Custom Power & Motor Control PCB

## Build

```bash
cd catkin_ws
catkin_make
source devel/setup.bash
```

## Running

Launch the required ROS nodes or use the provided startup script to initialize all system components.

## Applications

- Search and rescue
- Disaster response
- Autonomous exploration
- Robotics research

## Authors

- Bahar Kadıoğlu
- Ali Bölücü
- Emre Sağır
- Seha Altınkaynak
- Kıvanç Sadri Ünlüer

Department of Electrical and Electronics Engineering  
Gazi University
