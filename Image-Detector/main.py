import cv2 as cv
import numpy as np
import time
import zmq
import math
import sys, socket
import json
import base64
from network import UDPSender
from network import UDPReceiver
from imageProcessing import WristbandDetection

MAIN_IP_NUMBER = "127.0.0.1"
PYTHON_STREAMMING_PORT = 8051
UNITY_STREAMMING_PORT = 8052
PYTHON_RESPONSE_PORT = 8053

def Main():
    receiver = UDPReceiver(MAIN_IP_NUMBER, PYTHON_STREAMMING_PORT)
    sender = UDPSender(MAIN_IP_NUMBER, PYTHON_RESPONSE_PORT)
    while(True): 
        jsonData = receiver.TryToReceive()
        if not jsonData:
            print("NOT THING...")
            continue
        byteData = Base64Decode(jsonData["ImageData"])
        img = ReadImageFromBtyes(byteData)
        # Calculation -----------------------------
        data = WristbandDetection(img)
        print(data)
        if data:
            sender.Send(data)
        # -----------------------------------------

def Base64Decode(_string):
    return base64.b64decode(_string)

def ReadImageFromBtyes(_bytes):
    return cv.imdecode(np.frombuffer(_bytes, np.uint8), -1)

if __name__ == "__main__":
    Main()