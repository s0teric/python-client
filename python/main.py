#!/usr/bin/env python

import sys
import socket


# DEFAULTS
DEFAULT_IP = 'localhost'
DEFAULT_PORT = 19000


def main():
  tcpIp = DEFAULT_IP
  tcpPort = DEFAULT_PORT

  if len(sys.argv) > 3 : # Too many args
    print "More than two args supplied."
    print "main.py [ip address] [port]"
    print "main.py [ip address]"
    print "main.py"
    sys.exit(1)
  elif len(sys.argv) == 3: # file, ip address, port
    tcpIp = sys.argv[1]
    tcpPort = sys.argv[2]
  elif len(sys.argv) == 2: # file, ip address
    tcpIp = sys.argv[1]

  return
########## RUN MAIN ##########

if __name__ == '__main__':
    main()

