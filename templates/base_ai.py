# -*- python -*-
import socket

class BaseAI():

    def __init__(self):
        pass

    connection = None
    my_player_id = 0
    game_name = "${name}"

    #GLOBALS
% for datum in globals:
    ${datum.name} = None
% endfor

    #MODELS

% for model in models:
%   if model.type == "Model":
    ${lowercase(model.plural)} = []
%   endif
% endfor

    #GLOBALS ACCESSORS
% for datum in globals:
    #${datum.name}
    #${datum.doc}
    def get_${datum.name}(self):
        return self.${datum.name}
% endfor

