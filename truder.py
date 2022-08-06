from playsound import playsound
from threading import Thread
import numpy as np
import time
import speech_recognition as sr
from cvzone.SerialModule import SerialObject

arduino = SerialObject()

r = sr.Recognizer()

isplay = True

def play():
    global isplay
    global arduino
    playsound("poggers.mp3")
    isplay = True
    arduino.sendData([2])
    

c = 0

mic = sr.Microphone()

while True:
    with mic as source:
        try:
            #r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            sentence = r.recognize_google(audio)
            sentence = sentence.lower()
            if "intruder" in sentence and "alert" in sentence:
                 #print(isplay)
                 t = Thread(target=play, args=[])
                 if isplay:
                     t.start()
                     isplay = False
                     time.sleep(2)
                     arduino.sendData([1])
                 else:
                     pass
                
        except:
            pass#print("fat")
    arduino.sendData([0])


