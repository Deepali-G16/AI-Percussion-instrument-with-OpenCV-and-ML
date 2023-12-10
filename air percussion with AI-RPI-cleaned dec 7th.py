#Import the necessary Packages for this software to run
import mediapipe
import cv2
from collections import Counter
import pygame
import random
from time import sleep
import time
from pygame import mixer
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

pygame.init()
mixer.init()

music_note1 = pygame.mixer.Sound("/home/pi/Music/pi_music/tabla_na_o.wav")
music_note2 = pygame.mixer.Sound("/home/pi/Music/pi_music/tabla_na_s.wav")
music_note3 = pygame.mixer.Sound("/home/pi/Music/pi_music/tabla_tas3.wav")
music_note4 = pygame.mixer.Sound("/home/pi/Music/pi_music/loop_tabla.wav")
music_note5 = pygame.mixer.Sound("/home/pi/Music/pi_music/tabla_tas1.wav")


#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

#Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

h=480
w=640
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]
thumbs_up=0
start_time=0
elapsed_time=0
beat2=0


def findnameoflandmark(frame1):
     list=[]
     results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
     if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:


            for point in handsModule.HandLandmark:
                 list.append(str(point).replace ("< ","").replace("HandLandmark.", "").replace("_"," ").replace("[]",""))
     return list

def thumbs_up_to_Start(list):
      thumbs_up=0
      confirm_thumbs_up=0
      fingers=[]
      a=list
      if a[3][2] > a[4][2]: #making thumb up wrt to point 3
                             #[1:]this compares elements x of boht tht lists, if equal then compares y
             #       print ('thumbs up',b[4])
         thumbs_up=1

         fingers=[]
         for id in range(0,4):
            if a[tip[id]][2:] < a[tip[id]-2][2:]: 
             #  print(b[tipname[id]])

               fingers.append(1)

            else:
               fingers.append(0)
           

      #Below will print to the terminal the number of fingers that are up or down          
      x=fingers
      print('thumbs_up x',x)
      c=Counter(x)
      #print('thumbs_up counter(x)=',c)
      up=c[1]
      down=c[0]
    #  print('This many fingers are up - ', up)
    #  print('This many fingers are down - ',down)
      if thumbs_up==1 and x[0]==0 and x[1]==0:
         confirm_thumbs_up=1  #thumbs up only when thumb is up and pointer & middle finger down
             
      return(confirm_thumbs_up)
               
     

#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           thumbs_up=0
           
           ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           frame1 = cv2.resize(frame, (640, 480))
           
           #produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           list=[] #initializing position list before calling landmark
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           
           #Incase the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                  list=[]
                  for id, pt in enumerate (handLandmarks.landmark):
                      x = int(pt.x * w)
                      y = int(pt.y * h)
                      list.append([id,x,y])  #Gets landmarks position
                 
         # print('list=', list)
           a = list
           b= findnameoflandmark(frame1)
           

           if len(b and a)!=0:      #a[id,x,y]; x,y=[0,0] on top left of the screen; and x,y=[1,1] at the bottom right
                            
                if a[5][2] > a[4][2]: #making thumb up wrt to point 3
                             #[1:]this compares elements x of boht tht lists, if equal then compares y
                 #   print ('thumbs up',b[4])
                    #thumbs_up=1
                 pass
                                        
           
           if len(b and a)!=0:  #a[id,x,y]; x,y=[0,0] on top left of the screen; and x,y=[1,1] at the bottom right
         
               fingers=[]
               for id in range(0,4):
                  #If tip of finger is lower than tips of the other three fingers, then play sound for this finger 
                  if tip[id]==8:  #index_finger_tip landmark
                      if (a[tip[id]][2:] > a[11][2:]) and (a[tip[id]][2:] > a[15][2:]):
                          fingers.append(0)
                      else:
                          fingers.append(1)
                  if tip[id]==12:    #middle_finger_tip landmark
                      if (a[tip[id]][2:] > a[8][2:]) and (a[tip[id]][2:] > a[16][2:]) and (a[tip[id]][2:] > a[20][2:]):
                          fingers.append(0)
                      else:
                          fingers.append(1)
                  if tip[id]==16:      #ring_finger_tip landmark
                      if (a[tip[id]][2:] > a[7][2:]) and (a[tip[id]][2:] > a[11][2:]) and (a[tip[id]][2:] > a[20][2:]):
                          fingers.append(0)
                      else:
                          fingers.append(1)
                  if tip[id]==20:     #pinky_finger_tip landmark
                      if (a[tip[id]][2:] < a[tip[id]-1][2:]) or (a[tip[id]][2:] < a[tip[id]-2][2:]):
                          fingers.append(1)
                      else:
                          fingers.append(0)
                                                                                                               
                        
                #Below will print to the terminal the number of fingers that are up or down          
               x=fingers + finger
           #   print('x',x)
               c=Counter(x)
            #   print('counter(x)=',c)
               up=c[1]
               down=c[0]
             #  print('This many fingers are up - ', up)
             #  print('This many fingers are down - ',down)
              
                            
               if x[0] == 0: #pointer is down
                   music_note1.play()
                   GPIO.output(7,GPIO.HIGH)
                  
                                  
               if x[0] == 1: #pointer is up
                   music_note1.stop()
                   GPIO.output(7,GPIO.LOW)
            
               if x[1] == 0: #middle is down, play beat just once
                       music_note2.play()
                       GPIO.output(11,GPIO.HIGH)
                  
               
               if x[1] == 1: #pointer is down
                   music_note2.stop()
                   GPIO.output(11,GPIO.LOW)
               
               if x[2] == 0: #ring_finger is down
                   music_note3.play()
                   GPIO.output(13,GPIO.HIGH)
                  
               
               if x[2] == 1: #ring_finger is down
                   music_note3.stop()
                   GPIO.output(13,GPIO.LOW)
            
               if x[3] == 0: #pinky is down
                   music_note4.play()
                   GPIO.output(15,GPIO.HIGH)                           
              
               
               if x[3] == 1: #pinky is up
                   music_note4.stop()
                   GPIO.output(15,GPIO.LOW)            
                                
                            
               thumbs_up=0
               elapsed_time =0
               start_time=0
                  
            
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", frame1);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break

GPIO.cleanup()
