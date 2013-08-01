import socket
import struct


#Recieve string prefixed by uint32 length
def NetworkRecvString(conn):

    #Recieve 4 bytes for length
    prefix = conn.recv(4)
    print("Recv Prefix {}".format(prefix))
    length = struct.unpack('!I', prefix)
    print("Length {}".format(length))

    message = conn.recv(length)
    print("Recv Message {}".format(message))
    message = message.decode('utf-8')

    return message


#Send string prefixed by uint32 length
def NetworkSendString(conn, message):
    print("To send {}".format(message))
    message = message.encode('utf-8')
    print("Encoded {}".format(message))
    prefix = struct.pack('!I', len(message))
    print("Prefix {}".format(prefix))
    message = prefix + message
    print("Prefixed {}".format(message))

    conn.sendall(message)
    return True

