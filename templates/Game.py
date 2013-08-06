import time
import ClientJSON
from AI import *
import json
import sys
import GameObjects
import operator

class Game:

    def __init__(self, conn, addr, port, name):
        self.serv_conn = conn
        self.serv_addr = addr
        self.serv_port = port
        self.game_name = name
        self.ai = AI()
        self.ai.connection = self.serv_conn

    #Attempt to connect to the server
    def connect(self):
        while True:
            try:
                print("CLIENT: Attempting to connect...")
                self.serv_conn.connect((self.serv_addr, self.serv_port))
            except:
                print("CLIENT: Failed to connect.")
                time.sleep(1)
            else:
                print("CLIENT: Connected!")
                return True

    #Attempt to login to the server
    def login(self):

        loginJSON = ClientJSON.login.copy()
        loginJSON.get("args").update({"username": self.ai.username()})
        loginJSON.get("args").update({"password": self.ai.password()})

        try:
            print("CLIENT: Attempting to login...")
            Utility.NetworkSendString(self.serv_conn, json.dumps(loginJSON))

            print("CLIENT: Retrieving status from server...")
            data_string = Utility.NetworkRecvString(self.serv_conn)
            data_json = json.loads(data_string)
        except:
            print("CLIENT: Login failed.")
            print(sys.exc_info())
            return False
        else:
            if data_json.get("type", "failure") == "success":
                print("CLIENT: Login succeeded!")
                return True
            else:
                print("CLIENT: Login failed.")
                return False

    #Attempt to create a game on the server
    def create_game(self):

        create_gameJSON = ClientJSON.create_game.copy()
        if self.game_name is not None:
            create_gameJSON.get("args").update({"game_name": self.game_name})

        #ATTEMPT TO CREATE GAME
        try:
            print("CLIENT: Attempting to create a game...")
            Utility.NetworkSendString(self.serv_conn, json.dumps(create_gameJSON))

            print("CLIENT: Retrieving status from server...")
            data_string = Utility.NetworkRecvString(self.serv_conn)

            data_json = json.loads(data_string)
        except:
            print("CLIENT: Game creation failed.")
            print(sys.exc_info())
            return False
        else:
            if data_json.get("type", "failure") == "success":
                self.game_name = data_json.get("args").get("name")
                print("CLIENT: Game created: {}".format(self.game_name))
                return True
            else:
                print("CLIENT: Game creation failed.")
                return False

    #Receive Player ID from server
    def recv_player_id(self):
        try:
            print("CLIENT: Receive client's player id.")
            data_string = Utility.NetworkRecvString(self.serv_conn)
            data_json = json.loads(data_string)
        except:
            print("CLIENT: Failed to receive player id.")
            return False
        else:
            if data_json.get("type") == "player_id":
                self.ai.player_id = data_json.get("args").get("id")
                return True
            else:
                print("CLIENT: Failed to receive player id.")
                return False

    #Run when it is the Client's turn.
    def active_turn(self):
        print("CLIENT: Active turn.")
        self.ai.run()
        Utility.NetworkSendString(self.serv_conn, json.dumps(ClientJSON.next_turn))
        pass

    #Run when it is not the Client's turn.
    def inactive_turn(self):
        print("CLIENT: Inactive turn.")
        same_turn = True
        while same_turn:
            message = Utility.NetworkRecvString(self.serv_conn)

        return

    #Runs before main_loop has began.
    def init_main(self):
        print("CLIENT: Init main.")

        #Receive initial game state.
        try:
            print("CLIENT: Receiving initial game state.")
            message = Utility.NetworkRecvString(self.serv_conn)
        except:
            print("CLIENT: Unable to receive initial game state.")
        else:
            self.update_game(message)

        self.ai.init()
        return True

    #Runs after main_loop has finished.
    def end_main(self):
        print("CLIENT: End main.")
        self.ai.end()
        return True

    #Main connection loop until end of game.
    def main_loop(self):
        print("CLIENT: Main loop.")
        pass

    #Update game from message
    def update_game(self, message):
        try:
            message = json.loads(message)
        except:
            return False

        if message.get("type") != "changes":
            return False

        for change in message.get("args").get("changes"):
            if change.get("action") == "add":
                self.change_add(change)

            elif change.get("action") == "remove":
                self.change_remove(change)

            elif change.get("action") == "update":
                self.change_update(change)

            elif change.get("action") == "global_update":
                self.change_global_update(change)

% for model in models:
% if model.type == "Model":
        print( self.ai.${lowercase(model.plural)} )
% endif
% endfor
        return True

    #Parse the add action
    def change_add(self, change):
        values = change.get("values")
% for model in models:
% if model.type == "Model":
        if change.get("type") == "${model.name}":
            temp = GameObjects.${model.name}(\
% for datum in model.data:
${datum.name}=values.get("${datum.name}"),\
% endfor
)
            self.ai.${lowercase(model.plural)}.append(temp)
% endif
% endfor
        return True

    #Parse the remove action.
    def change_remove(self, change):
        remove_id = change.get("id")
% for model in models:
% if model.type == "Model":
        try:
            index = self.ai.${lowercase(model.plural)}.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.${lowercase(model.plural)}.remove(index)
            return True
% endif
% endfor
        return False

    #Parse the update action.
    def change_update(self, change):
        change_id = change.get("id")
        values = change.get("values")
% for model in models:
% if model.type == "Model":
        try:
            index = self.ai.${lowercase(model.plural)}.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.${lowercase(model.plural)}[index].__dict__.update(values)
            return True
% endif
% endfor
        return False

    #Parse the global_update action
    def change_global_update(self, change):
        values = change.get("values")
        self.ai.__dict__.update(values)
        pass

    def run(self):
        if not self.connect(): return False
        if not self.login(): return False
        if not self.create_game(): return False
        if not self.recv_player_id(): return False
        if not self.init_main(): return False
        if not self.main_loop(): return False
        if not self.end_main(): return False