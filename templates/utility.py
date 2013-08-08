import socket
import struct


#Recieve string prefixed by uint32 length
def receive_string(conn):

    #Recieve 4 bytes for length
    prefix = conn.recv(4)
    length = struct.unpack('!I', prefix)[0]
    message = conn.recv(length)
    message = message.decode('utf-8')

    print("--- RECEIVED ---")
    print(message)
    return message


#Send string prefixed by uint32 length
def send_string(conn, message):
    print("--- SEND ---")
    print(message)
    message = message.encode('utf-8')
    prefix = struct.pack('!I', len(message))
    message = prefix + message
    conn.sendall(message)

    return

