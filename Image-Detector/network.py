import sys, socket
import json

BUFFER_SIZE = 65535

class UDPSender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def Send(self, data):
        message = json.dumps(data)
        self.socket.sendto(bytes(message, "utf-8"), (self.ip, self.port))

class UDPReceiver:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def TryToReceive(self):
        jsonString = self.sock.recvfrom(BUFFER_SIZE)[0].decode('utf-8')
        data = None
        if jsonString:
            data = json.loads(jsonString)
        return data
