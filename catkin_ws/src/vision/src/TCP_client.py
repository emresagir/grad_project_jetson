#!/usr/bin/env python3

import time
import socket
import os
import rospy
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#HOST = "127.0.0.1"
HOST = "20.203.172.10"
PORT = 8078

absolute_path = os.path.dirname(os.path.abspath(__file__))
upper_directory = os.path.dirname(absolute_path)

#upper ile değiştir
folderPathCV = os.path.join(absolute_path, "imagesCV")
folderPathMap = os.path.join(absolute_path, "imagesMap")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((HOST, PORT))


def send(event):
    
	file_path = event.src_path
	file_name = os.path.basename(file_path)
	folder_name = os.path.basename(os.path.dirname(file_path))
 

	file = open(file_path, 'rb')
	imageSize = os.path.getsize(file_path)
 
	messageFolderName ='{:0>15}'.format(folder_name)
	client_socket.send(messageFolderName.encode('latin-1'))
 
	messageName ='{:0>50}'.format(file_name)
	client_socket.send(messageName.encode('latin-1'))

	str_imageSize = '{:0>15}'.format(str(imageSize))
	client_socket.send(str_imageSize.encode())
	print("Image Size: " + str(imageSize) + "\n")

	totalPacketSize = 9 + 512*40 + 9
	TCP_PacketNumber = 1
	packetSize = 256
	localChecksum = 0
	TCP_Checksum = 0

	TCP_BytesReceived = 0
	TCP_TotalBytesReceived = 0
	TCP_TotalPacketNumber = imageSize // packetSize + (1 if imageSize % packetSize > 0 else 0)

	imageData = file.read()

	for i in range(0, len(imageData) , packetSize):
					
		str_TCP_PacketNumber = '{:#>9}'.format(str(TCP_PacketNumber))
		client_socket.send(str_TCP_PacketNumber.encode())
		print( str(TCP_PacketNumber))
		
		
		packet = imageData[i:i+packetSize]
		# for the last packet
		if len(packet) < packetSize:
			packet += b'\x00' * (packetSize - len(packet))
		client_socket.send(packet)

				
		TCP_Checksum = 0
		for a in range(0, packetSize):
			TCP_Checksum += packet[a]
		str_TCP_Checksum = '{:#>9}'.format(str(TCP_Checksum))
		client_socket.send(str_TCP_Checksum.encode())

		print(str(TCP_Checksum) + "\n")
		
		if ((TCP_PacketNumber % 20) == 0) or (TCP_PacketNumber == TCP_TotalPacketNumber):
			ACK_NCK = client_socket.recv(4).decode('latin-1')
			print(ACK_NCK + "\n")
   
		TCP_PacketNumber += 1
		
	file.close()
 
	print("-- END OF SEND --")

class FileModifiedHandler(LoggingEventHandler):
		




        
    def on_modified(self, event):
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        folder_path = os.path.dirname(file_path)
        print(file_path)
        time.sleep(1)
        send(event)


def on_created(event):
    file_path = event.src_path
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)
    print(file_path)
    time.sleep(1)
    send(event)


if __name__ == "__main__":
    rospy.init_node("tcp")
    
    messageCom = "Recv"
    messageCom ='{:0>10}'.format(messageCom)
    client_socket.send(messageCom.encode('latin-1'))
 
    event_handler1 = LoggingEventHandler()
    event_handler2 = LoggingEventHandler()
    
    event_handler1.on_created = on_created
    event_handler2.on_created = on_created
 
    observer1 = Observer()
    observer2 = Observer()
 
    observer1.schedule(event_handler1, folderPathCV, recursive=True)
    observer2.schedule(event_handler2, folderPathMap, recursive=True)
 
    observer1.start()
    observer2.start()
 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer1.stop()
        observer2.stop()

    observer1.join()
    observer2.join()
 
	
