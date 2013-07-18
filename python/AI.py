# -*- python -*-
from BaseAI import BaseAI
from GameObjects import *

class AI(BaseAI):
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  def init(self):
    pass

  def end(self):
    pass

  def run(self):
    pass

  def __init__(self):
    BaseAI.__init__(self)