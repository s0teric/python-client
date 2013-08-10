import socket
import struct

verbose = False
very_verbose = False

#Recieve string prefixed by uint32 length
def receive_string(conn):

    #Recieve 4 bytes for length
    prefix = conn.recv(4)
    length = struct.unpack('!I', prefix)[0]
    message = conn.recv(length)
    message = message.decode('utf-8')

    vv_print("Received: {}".format(message))

    return message


#Send string prefixed by uint32 length
def send_string(conn, message):

    vv_print("Sending: {}".format(message))

    message = message.encode('utf-8')
    prefix = struct.pack('!I', len(message))
    message = prefix + message
    conn.sendall(message)

    return

#Verbose print
def v_print(message):
    if verbose or very_verbose:
        print(message)
    return True

def vv_print(message):
    if very_verbose:
        print(message)
    return True

