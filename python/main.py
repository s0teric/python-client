#!/usr/bin/env python

import sys
import time
import socket
import json
import ClientJSON



# DEFAULTS
DEFAULT_IP, DEFAULT_PORT = "localhost", 19000


def main():
  tcpIp, tcpPort = DEFAULT_IP, DEFAULT_PORT

  if len(sys.argv) > 3 : # Too many args
    print("More than two args supplied.")
    print("main.py [ip address] [port]")
    print("main.py [ip address]")
    print("main.py")
    sys.exit(1)
  elif len(sys.argv) == 3: # file, ip address, port
    tcpIp = str(sys.argv[1])
    tcpPort = int(sys.argv[2])
  elif len(sys.argv) == 2: # file, ip address
    tcpIp = str(sys.argv[1])

  connection = None

  ClientJSON.login.get("args").update({"username": "Ruski"})
  ClientJSON.login.get("args").update({"password": "Malooski"})

  #ATTEMPT TO CONNECT TO SERVER
  connected = False
  while not connected:
    try:
      print("Attempting to connect...")
      connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      connection.connect((tcpIp, tcpPort))
    except:
      print("Failed to connect.")
      #connection.close()
      time.sleep(1)
    else:
      print("Connected!")
      connected = True

  #ATTEMPT TO LOG IN TO SERVER
  try:
    print("Attempting to login...")
    connection.sendall(json.dumps(ClientJSON.login))

    print("Retrieving status from server...")
    data_string = connection.recv(1024)
    print(data_string)
    data_json = json.loads(data_string)
    print(data_json)
  except:
    print("Login failed.")
    sys.exit(1)
  else:
    if data_json.get("status") == "success":
      print("Login succeeded!")
    else:
      print("Login failed.")
      sys.exit(1)


  #ATTEMPT TO CREATE GAME ON THE SERVER

  print("Closing connection.")
  connection.close()

  return



########## RUN MAIN ##########
if __name__ == '__main__':
  main()
