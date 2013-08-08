# -*- python -*-
from base_ai import BaseAI


class AI(BaseAI):
    username = "Shell AI"

    password = "password"

    def init(self):
        pass

    def end(self):
        pass

    def run(self):
        for player in self.players:
            player.talk("PLAYER TALK MESSAGE")
        pass

    def __init__(self):
        BaseAI.__init__(self)
