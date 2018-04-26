from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus
import time
import cv2
import numpy as np

#adresse I2C
bus=smbus.SMBus(1)
adress=0x03






""" premiere methode detection de ligne"""





def ligne (cropped, flagD, flagDD, flagG, flagA, flagDG, contours):

    if len(contours) > 0:
         M=cv2.moments(contours[0])

         cx=int(M['m10']/M['m00'])
         cy= int(M['m01']/M['m00'])
         
         cv2.circle(cropped,(cx,cy),15,(0,255, 0),5)
         
         
         

         if cx>725 :

             if cx>1150:
                 if flagD ==0:
                     print("droite")
                     bus.write_byte(adress,2)
                     time.sleep(0.01)
                     flagD =1
                     flagDD=0
                     flagG=0
                     flagDG=0
                     flagA=0
             else :
                 if flagDD ==0 :
                     print("demi-droite")
                     bus.write_byte(adress,8)
                     time.sleep(0.01)
                     flagDD=1
                     flagD =0
                     flagG=0
                     flagDG=0
                     flagA=0
             
         
             
         elif ( cx<524):

            if cx<50 :
                if flagG ==0 :
                    print("gauche")
                    bus.write_byte(adress,1)
                    time.sleep(0.01)
                    flagG=1
                    flagDG=0
                    flagD =0
                    flagDD=0
                    flagA= 0

            else :
                 if flagDG ==0 :
                     print("demi-gauche")
                     bus.write_byte(adress,7)
                     time.sleep(0.01)
                     flagDG=1
                     flagD =0
                     flagDD=1
                     flagG=0
                     flagA=0
         else :
             if flagA ==0 :
                 print("avant")
                 bus.write_byte(adress,3)
                 time.sleep(0.01)
                 flagA=1
                 flagG=0
                 flagDG=0
                 flagD=0
                 flagDD=0
             
    else :
         print("No Centroid Found")



    return flagDG, flagD, flagDD, flagG, flagA












""" deuxieme methode detection de ligne"""






def ligne2 (cropped, contours):
    
      if len(contours) > 0:
         M=cv2.moments(contours[0])

         cx=int(M['m10']/M['m00'])
         cy= int(M['m01']/M['m00'])
 
         cv2.circle(cropped,(cx,cy),15,(0,255, 0),5)

         val=1250-cx

         cx2=int(val*46/1250 + 67)

         bus.write_byte(adress,cx2)
         
         time.sleep(0.01)
         return cx2
