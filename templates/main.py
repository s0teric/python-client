#!/usr/bin/env python

import socket
import argparse
import utility
from game import Game


def main():
    parser = argparse.ArgumentParser(description="Python client for SIG-GAME framework.")
    parser.add_argument("-a", "--address", dest='conn_address', default="localhost",
                        help="The address of the game server.", type=str)
    parser.add_argument("-p", "--port", dest='conn_port', default="19000",
                        help="The port of the game server.", type=int)
    parser.add_argument("-g", "--game", dest='game_name', default=None,
                        help="The name of game to connect to on the server.")

    parser.add_argument("-v", "--verbose", dest='is_verbose', default=False,
                        help="Print more output messages.", action="store_true")
    parser.add_argument("-vv", "--very-verbose", dest='is_very_verbose', default=False,
                        help="Print even more output messages.", action="store_true")
    args = parser.parse_args()

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    game = Game(conn=connection, addr=args.conn_address, port=args.conn_port, name=args.game_name)
    utility.verbose = args.is_verbose
    utility.very_verbose = args.is_very_verbose

    game.run()

    connection.close()

    return


########## RUN MAIN ##########
if __name__ == '__main__':
    main()
