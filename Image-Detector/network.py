import sys, socket
import json

class UDPSender():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def Send(self, data):
        message = json.dumps(data)
        self.sock.sendto(bytes(message, "utf-8"), (self.ip, self.port))