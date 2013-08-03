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
        pass #sys.exit(1)

    if not login(conn=connection):
        pass #sys.exit(1)

    if not create_game(conn=connection):
        pass #sys.exit(1)

    if not main_loop(conn=connection):
        pass #sys.exit(1)

    print("Closing connection.")
    connection.close()

    return


def connect(conn, addr, port):
    while True:
        try:
            print("CLIENT: Attempting to connect...")
            conn.connect((addr, port))
        except:
            print("CLIENT: Failed to connect.")
            time.sleep(1)
        else:
            print("CLIENT: Connected!")
            return True


def login(conn):

    loginJSON = ClientJSON.login.copy()
    loginJSON.get("args").update({"username": AI.username()})
    loginJSON.get("args").update({"password": AI.password()})

    try:
        print("CLIENT: Attempting to login...")
        Utility.NetworkSendString(conn, json.dumps(loginJSON))

        print("CLIENT: Retrieving status from server...")
        data_string = Utility.NetworkRecvString(conn)
        data_json = json.loads(data_string)
    except:
        print("CLIENT: Login failed.")
        print(sys.exc_info())
        return False
    else:
        if data_json.get("type") == "success":
            print("CLIENT: Login succeeded!")
            return True
        else:
            print("CLIENT: Login failed.")
            return False


def create_game(conn):

    create_gameJSON = ClientJSON.create_game.copy()

    try:
        print("CLIENT: Attempting to create a game...")
        Utility.NetworkSendString(conn, json.dumps(create_gameJSON))

        print("CLIENT: Retrieving status from server...")
        data_string = Utility.NetworkRecvString(conn)
        data_json = json.loads(data_string)
    except:
        print("CLIENT: Game creation failed.")
        print(sys.exc_info())
        return False
    else:
        if data_json.get("type") == "success":
            print("CLIENT: Game creation successful!")
            return True
        else:
            print("CLIENT: Game creation failed.")
            return False


def main_loop(conn):
    while True:
        message = Utility.NetworkRecvString(conn)


def updateGame(message):
    additions = []
    global_changes = {}
    changes = []
    removals = []





    pass

########## RUN MAIN ##########
if __name__ == '__main__':
    main()
