import cv2 as cv
import numpy as np
import time
import zmq
import math
import sys, socket
import json
from network import UDPSender
from imageProcessing import WristbandDetection


def cameraCapture():
    sender = UDPSender("127.0.0.1", 8051)
    cam = cv.VideoCapture(0)
    while(True):  
        _, img = cam.read()
        # Calculation -----------------------------
        data = WristbandDetection(img)
        # print(data)
        if data:
            sender.Send(data)
        # -----------------------------------------
        cv.imshow('main', img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def ConfigWaiting():
    while True:
        print("")

if __name__ == "__main__":
    print("Hi")
    # ConfigWaiting()
    cameraCapture()
    