from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus
import time
import cv2
import numpy as np

#adresse I2C
bus=smbus.SMBus(1)
adress=0x1a





""" premiere methode detection du feux """



def feu(im_gray,flag, image):                  

    #detection feu rouge

    templateFeu = cv2.imread('feu_rouge.png',0)

    

    
    wF, hF = templateFeu.shape[::-1]
    resFeu =cv2.matchTemplate(im_gray, templateFeu ,cv2.TM_CCOEFF_NORMED)
    thresholdFeu = 0.6
    locFeu= np.where( resFeu >= thresholdFeu)
    if np.any( resFeu >= thresholdFeu):
        print("feu rouge")
        bus.write_byte(adress,6)
        time.sleep(5)
        flag =0
        print("flag : ", flag)
        if flag ==0 :
            bus.write_byte(adress,4)
            print("avancer")
            time.sleep(1)
            flag =1
    else :
        if flag ==0:
            print("avancer")
            bus.write_byte(adress,4)
            flag =1
    for pt in zip(*locFeu[::-1]):
                cv2.rectangle(image, pt, (pt[0]+wF,pt[1]+hF),(0,0,255),2)


    return flag








""" premiere methode detection du stop """


def stop(im_gray,flag, image):

    #detection stop

    template = cv2.imread('stop.png',0)
    
    
    w, h = template.shape[::-1]
    res =cv2.matchTemplate(im_gray, template ,cv2.TM_CCOEFF_NORMED)
    threshold = 0.3
    loc= np.where( res >= threshold)
    if np.any( res >= threshold):
        print("stop")
        bus.write_byte(adress,2)
        time.sleep(5)
        flag =0
        
        if flag ==0:
            bus.write_byte(adress,1)
            time.sleep(0.1)
            print("avancer")
            
            flag =1
    else :
        
        if flag ==0:
            print("avancer_stop")
            bus.write_byte(adress,1)
            time.sleep(0.5)
            flag =1
    for pt in zip(*loc[::-1]):
                  cv2.rectangle(image, pt, (pt[0]+w,pt[1]+h),(0,0,255),2)

    return flag






""" deuxieme methode detection du stop """





def stop2(hsv2,flag, image):

    lower_red=np.array([115, 160, 120])
    upper_red=np.array([140, 255, 200])
    mask2=cv2.inRange(hsv2, lower_red,upper_red )

    kernel_erode2 = np.ones((4,4), np.uint8)
    eroded_mask2 =cv2.erode(mask2,kernel_erode2,iterations=1)
    kernel_dilate2 = np.ones((6,6), np.uint8)
    dilated_mask2 =cv2.dilate(eroded_mask2, kernel_dilate2, iterations=1)

    contours2,hierarchy = cv2.findContours(dilated_mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2 = sorted(contours2,key=cv2.contourArea, reverse=True)[:1]

    if len(contours2) > 0:
         M2=cv2.moments(contours2[0])

         cx2=int(M2['m10']/M2['m00'])
         cy2= int(M2['m01']/M2['m00'])


         cv2.circle(hsv2,(cx2,cy2),15,(255,0, 0),5)
         print"stop"
         bus.write_byte(adress,2)
         time.sleep(0.1)
         bus.write_byte(adress,1)
         time.sleep(0.1)
         flag=1

    

    return flag
