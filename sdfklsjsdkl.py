from playsound import playsound
import cv2
from cvzone.ClassificationModule import Classifier
from threading import Thread
import numpy as np
import time
from cvzone.SerialModule import SerialObject

arduino = SerialObject()

isplay = True

def play():
    global isplay
    global arduino
    arduino.sendData([1])
    playsound("poggers.mp3")
    isplay = True
    arduino.sendData([2])
    

cap = cv2.VideoCapture(0)

classifier = Classifier('keras_model.h5', 'labels.txt')

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

c = 0

while True:
    success, img = cap.read()
    #img = cv2.imread("darwin.png")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)
    if len(faces) >= 1:
        for (x, y, width, height) in faces:
            cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 1)
            pts1 = np.float32([[x,y],[x+width,y],[x,y+ width],[x+width,y+width]])
            pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
            matrix=cv2.getPerspectiveTransform(pts1,pts2)
            finimg = cv2.warpPerspective(img,matrix,(width,height))
            load = cv2.resize(finimg, (128, 128))
            cv2.imshow('face', finimg)
            c += 1
            

        predictions = classifier.getPrediction(finimg)
        print(predictions)
        if predictions[0][0] >= 0.9:
            pass
        else:
             t = Thread(target=play, args=[])
             if isplay:
                 t.start()
                 isplay = False
             else:
                 pass
             
        cv2.waitKey(1)
        arduino.sendData([0])

