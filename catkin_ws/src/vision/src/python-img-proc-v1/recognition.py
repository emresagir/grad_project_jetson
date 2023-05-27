#!/usr/bin/env python3 
import face_recognition
import os, sys
import cv2
import numpy as np
import math
import rospy
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images

#inner rectangle elimination function
def UnifyRectangleWithIntersection (vec_rect_list):
    vec_groups = []
    if len(vec_rect_list) == 0:
        print("Vector size should be greater than zero")

    elif len(vec_rect_list) == 1:
        vec_groups.extend(vec_rect_list)

    else:
        rect_idx = 0
        while rect_idx < len(vec_rect_list):
            reference_rect = vec_rect_list[rect_idx]
            if len(vec_groups) == 0:
                vec_groups.append(reference_rect)
            else:
                bash_group = False
                group_idx = 0
                while group_idx < len(vec_groups):
                    #intersection_area = vec_groups[group_idx] and reference_rect
                    intersection_area = area(vec_groups[group_idx], reference_rect)
                    if intersection_area > 0:
                        print("before: ", vec_groups[group_idx][2]*vec_groups[group_idx][3])
                        #vec_groups[group_idx] = (vec_groups[group_idx] or reference_rect)
                        vec_groups[group_idx] = union(vec_groups[group_idx],reference_rect)
                        print("after: ", vec_groups[group_idx][2] * vec_groups[group_idx][3])
                        bash_group = True
                        break
                    group_idx +=1

                if bash_group == False:
                    vec_groups.append(reference_rect)
            rect_idx +=1
    return vec_groups

#########################################################################
def union(a,b):
  x = min(a[0], b[0])
  y = min(a[1], b[1])
  w = max(a[0]+a[2], b[0]+b[2]) - x
  h = max(a[1]+a[3], b[1]+b[3]) - y
  return (x, y, w, h)

def intersection(a,b):
  x = max(a[0], b[0])
  y = max(a[1], b[1])
  w = min(a[0]+a[2], b[0]+b[2]) - x
  h = min(a[1]+a[3], b[1]+b[3]) - y
  if w<0 or h<0:
      return ()
  return (x, y, w, h)

def area(a,b):
  x = max(a[0], b[0])
  y = max(a[1], b[1])
  w = min(a[0]+a[2], b[0]+b[2]) - x
  h = min(a[1]+a[3], b[1]+b[3]) - y
  if w<0 or h<0:
      return (0)
  return (w*h)
##########################################################

# face_match doğruluk oranı
def face_confidence(face_distance, face_match_threshold=0.7):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

#########################################################################


#Converting ros image data to cv data.
def callback(data):
  rospy.loginfo("Buraya GELDİ")
  global current_frame
 
  # Used to convert between ROS and OpenCV images
  br = CvBridge()
 
  # Output debugging information to the terminal
  rospy.loginfo("receiving video frame")
   
  # Convert ROS Image message to OpenCV image
  current_frame = br.imgmsg_to_cv2(data)
   
  # Display image
  #cv2.imshow("camera", current_frame)
   
  #cv2.waitKey(1)
  
  fr.run_recognition()
  cv2.waitKey(1)


##################################################################
#TODO: BAHAR Buradan aldığımız frame'i kullanmamız gerekiyor kod içerisinde.






class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    counter = 0

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('/home/jetson/grad_project_jetson/catkin_ws/src/vision/src/python-img-proc-v1/faces'):
            face_image = face_recognition.load_image_file(f"/home/jetson/grad_project_jetson/catkin_ws/src/vision/src/python-img-proc-v1/faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        #Our video frames will be subscribed from another node (EMRE) so this code will be commented.
        ####################################
        #video_capture = cv2.VideoCapture(0) 
        #video_capture = cv2.VideoCapture("C:/Users/User/Desktop/green_screen_queen.webm")


        #if not video_capture.isOpened():
        #    sys.exit('Video source not found...')
        ##########################################

        #Subscribed message goes to callback function and turns as a opencv image.
        
        


        #while True:
        

        rospy.loginfo("HOPPPALAAAA")
        #ret, frame = video_capture.read()
        frame = current_frame ## TODO = GLOBAL DEĞİŞKEN OLARAK BELİRLEMEMİZ GEREKİYOR.

        # Only process every other frame of video to save time
        if self.process_current_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'

                # Calculate the shortest distance to face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                self.face_names.append(f'{name}    ({confidence})')

        self.process_current_frame = not self.process_current_frame

        # Display the results,,, size selection for recognition screen
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Create the frame with the name
            cv2.rectangle(frame, (left, top), (right, bottom), (186,85,211), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (186,85,211), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            img_name = name[:7]
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            absolute_path = os.path.join(path, "imagesCV")
            
            
            self.counter += 1
            if counter % 20 == 0:
                cv2.imwrite(os.path.join(absolute_path,img_name + '_' + str(int(self.counter/20))+'.jpg'), frame)

#############################################################################
#############################################################################

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Kırmızı renk aralığında pikselleri tespit et
        lower_red = np.array([0, 155, 70])
        upper_red = np.array([10, 255, 255])
        red1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([160, 155, 70])
        upper_red = np.array([179, 255, 255])
        red2 = cv2.inRange(hsv, lower_red, upper_red)

        maskRed = cv2.addWeighted(red1, 1, red2, 1, 0.0)
        maskRed_erosion = cv2.erode(maskRed, np.ones((5, 5), np.uint8), 4)
        Red_canny = cv2.Canny(maskRed_erosion, 50, 100)

        #####################################################################

        # yeşil renk aralığında pikselleri tespit et
        lower_green = np.array([50, 80, 90])  # (40, 40,40) ~ (70, 255,255)
        upper_green = np.array([86, 255, 255])

        maskGreen = cv2.inRange(hsv, lower_green, upper_green)
        maskGreen_erosion = cv2.erode(maskGreen, np.ones((5, 5), np.uint8), 2)
        # erosion removes pixels on object boundaries
        Green_canny = cv2.Canny(maskGreen_erosion, 100, 200)  # canny used for edge detection

        # Kırmızı renk aralığında piksellerin sayısını hesapla
        count1 = cv2.countNonZero(maskRed_erosion)
        count2 = cv2.countNonZero(maskGreen_erosion)

        # Eğer kırmızı renk aralığında pikseller var ise, ilerlemeyi durdur
        if count1 > 0 and count2 > 0:
            cv2.putText(frame, 'KIRMIZI VE YESiL RENK TESPiT EDiLDi. iLERLEME DURDU', (60, 400),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2, cv2.LINE_4)

        elif count1 > 0:
            # print('Kırmızı renk tespit edildi. İlerleme durduruldu.')
            cv2.putText(frame, 'KIRMIZI RENK TESPiT EDiLDi. iLERLEME DURDU', (20, 400),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2, cv2.LINE_4)

        elif count2 > 0:
            # print('yeşil renk tespit edildi.İlerleme devam ediyor.')
            cv2.putText(frame, 'YESiL RENK TESPiT EDiLDi. iLERLEMEYE DEVAM', (20, 400),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2, cv2.LINE_4)

        else:
            cv2.putText(frame, 'KIRMIZI YA DA YESiL RENK BULUNAMADI. iLERLEMEYE DEVAM ', (60, 400),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2, cv2.LINE_4)

    #########################################################################

        # Maskeyi kullanarak görüntüdeki kırmızı renkleri tespit et
        contours1, _ = cv2.findContours(Red_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rectangles1 = []

        # Kontürler üzerinde döngüye girerek dikdörtgenleri oluştur
        for cnt1 in contours1:
            # Kontürün çevresindeki dikdörtgeni oluştur
            x1, y1, w1, h1 = cv2.boundingRect(cnt1)
            # Dikdörtgeni vektöre ekle
            rectangles1.append([x1, y1, w1, h1])

        vec_groups_first_pass1 = UnifyRectangleWithIntersection(rectangles1)
        vec_groups_second_pass1 = UnifyRectangleWithIntersection(vec_groups_first_pass1)

        for rect1 in vec_groups_second_pass1:
            x1, y1, w1, h1 = rect1
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)

    ##########################################################################

        # Maskeyi kullanarak görüntüdeki yeşil renkleri tespit et
        contours2, _ = cv2.findContours(Green_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rectangles2 = []

        # Kontürler üzerinde döngüye girerek dikdörtgenleri oluştur
        for cnt2 in contours2:
            # Kontürün çevresindeki dikdörtgeni oluştur
            x2, y2, w2, h2 = cv2.boundingRect(cnt2)
            # Dikdörtgeni vektöre ekle
            rectangles2.append([x2, y2, w2, h2])

        vec_groups_first_pass2 = UnifyRectangleWithIntersection(rectangles2)
        vec_groups_second_pass2 = UnifyRectangleWithIntersection(vec_groups_first_pass2)

        for rect2 in vec_groups_second_pass2:
            x2, y2, w2, h2 = rect2
            cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
    
        
    ############################################################################

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)
        #cv2.imshow('rect_process', frame1)

        rospy.loginfo("*************************************")
        #rospy.Subscriber('video_frames', Image, callback)
        
        
        
        # Hit 'q' on the keyboard to quit!
        #if cv2.waitKey(1) == ord('q'):
        #    break
                
        # Release handle to the webcam
        #video_capture.release()
        #cv2.destroyAllWindows()
    
        

if __name__ == '__main__':
    rospy.init_node("vision" )
    rospy.loginfo("WASSUP ̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿ ")
    fr = FaceRecognition()
    
    rospy.Subscriber('video_frames', Image, callback) 
            
    rospy.spin()
