# -*- python -*-

class Game:
% for datum in globals:
  ${lowercase(datum.plural)} = []