import socket
import struct

#Recieve a string-JSON message from the server
def NetworkGetMessage(conn):
  import socket

  #Recieve 4 bytes for length
  prefix = conn.recv(4)
  length = NetworkPrefixLength(prefix)
  message = conn.recv(length)

  return message

#Send a string-JSON message to the server by prefixing uint32 network byte order
def NetworkSendMessage(conn, message):
  prefixed = repr(struct.pack('!I', len(message))) + message
  conn.sendall(prefixed)
  return

#Get the length of the network message from a uint32 network byte order
def NetworkPrefixLength(message):
  length = struct.unpack('!I', message)
  return length

