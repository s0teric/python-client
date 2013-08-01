#!/usr/bin/env python

import sys
import time
import socket
import json
import ClientJSON
from AI import *
import argparse
import Utility


def main():
    parser = argparse.ArgumentParser(description="Python client for SIG-GAME framework.")
    parser.add_argument("-a", "--address", dest='conn_address', default="localhost",
                        help="The address of the game server.", type=str)
    parser.add_argument("-p", "--port", dest='conn_port', default="19000",
                        help="The port of the game server.", type=int)
    parser.add_argument("-n", "--number", dest='game_number', default="0",
                        help="The number of game to connect to on the server.", type=int)
    args = parser.parse_args()

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if not connect(connection, args.conn_address, args.conn_port):
        sys.exit(1)

    if not login(conn=connection):
        pass #sys.exit(1)

    if not create_game(conn=connection):
        sys.exit(1)

    print("Closing connection.")
    connection.close()

    return


def connect(conn, addr, port):
    while True:
        try:
            print("Attempting to connect...")
            conn.connect((addr, port))
        except:
            print("Failed to connect. {}".format(sys.exc_info()))
            time.sleep(1)
        else:
            print("Connected!")
            return True

def login(conn):

    loginJSON = ClientJSON.login.copy()
    loginJSON.get("args").update({"username": AI.username()})
    loginJSON.get("args").update({"password": AI.password()})

    try:
        print("Attempting to login...")
        Utility.NetworkSendString(conn, json.dumps(loginJSON))

        print("Retrieving status from server...")
        data_string = Utility.NetworkRecvString(conn)
        print(data_string)

        data_json = json.loads(data_string)
    except:
        print("Login failed.")
        print(sys.exc_info())
        return False
    else:
        if data_json.get("type") == "success":
            print("Login succeeded!")
            return True
        else:
            print("Login failed. {}".format("Failed to parse server message."))
            return False


def create_game(conn):
    create_gameJSON = ClientJSON.create_game.copy()

    try:
        print("Attempting to create a game...")
        Utility.NetworkSendString(conn, json.dumps(create_gameJSON))

        print("Retrieving status from server...")
        data_string = Utility.NetworkRecvString(conn)
        print(data_string)

        data_json = json.loads(data_string)
    except:
        print("Game creation failed.")
        print(sys.exc_info())
        return False
    else:
        print("Game creation successful!")
        return True


########## RUN MAIN ##########
if __name__ == '__main__':
    main()
