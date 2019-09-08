import sys, socket

ip = "127.0.0.1"
port = 8051
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes("ddd", "utf-8"), (ip, port))
