from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
from fonction import *
from ligne import *
import RPi.GPIO as gpio
import sys
import smbus
import time
import cv2
import numpy as np


adress=0x03

#adresse I2C
bus=smbus.SMBus(1)

time.sleep(2)
print("adresse I2C", adress)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
flag =0
flagAV =0
camera=PiCamera()
camera.resolution=(1250, 600)#L*H
camera.framerate=49
rawCapture = PiRGBArray(camera, size=(1250,600))



time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):



    """ traitement d'images """
    
    image = frame.array

    key =cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)

    im_gray=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    hsv2 = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    (thresh, im_bw) =cv2.threshold(im_gray, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    
    hsv2 = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    cropped = image [500:600 , 1:1250]
    invGamma = 10
    table = np.array([((i / 255.0) ** invGamma) * 255
	for i in np.arange(0, 256)]).astype("uint8")
    test2 =cv2.LUT(cropped, table)
    hsv = cv2.cvtColor(test2, cv2.COLOR_RGB2HSV)
    ret, seuil =cv2.threshold (hsv, 0,255,0)
    lower_white=np.array([0, 0, 150])
    upper_white=np.array([230, 230, 255])
    mask=cv2.inRange(hsv, lower_white, upper_white)
    test = cv2.bitwise_and(cropped, cropped, mask=mask)
    kernel_erode = np.ones((4,4), np.uint8)
    eroded_mask =cv2.erode(mask,kernel_erode,iterations=1)
    kernel_dilate = np.ones((6,6), np.uint8)
    dilated_mask =cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    contours,hierarchy = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=cv2.contourArea, reverse=True)[:1]



    """ demarrage moteur """

    if flagAV==0 :
        bus.write_byte(adress,1)
        print("marche")
        time.sleep(0.01)
        flagAV=1



    """ ligne blanche """
        
    cx2=ligne2(cropped, contours)
    print("cx2", cx2)




    """ fonction pour le stop """""
    
    if flag==0 :
        flag=stop2(hsv2, flag, image)
        if flag==1 :
         bus.write_byte(adress,2)
         time.sleep(3)
         bus.write_byte(adress,1)
         time.sleep(0.1)
    







    """ affichage des frames



    cv2.imshow("Frame",image)
    cv2.imshow("cropped", cropped)
    cv2.imshow("Fram2e",hsv2)
    """
    
