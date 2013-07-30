import socket
import sys
import time

HOST, PORT = "localhost", 16000

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    while True:
      received = sock.recv(1024)
      print("Received: {}".format(received))
      time.sleep(.1)
finally:
    sock.close()
