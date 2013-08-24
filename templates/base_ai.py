# -*- python -*-
import socket

#\
# @class BaseAI
#  @brief Class to store competitor-accessible data and functions


class BaseAI():

    def __init__(self):
        pass

    connection = None
    game_name = "${name}"

    #\
    # @var my_player_id
    #  @breif The player_id of the competitor.
    my_player_id = 0

% for datum in globals:
    #\
    # @var ${datum.name}
% if datum.doc:
    #  @brief ${datum.doc}
% endif
    ${datum.name} = None

% endfor

% for model in models:
%   if model.type == "Model":
    #\
    #  @var ${lowercase(model.plural)}
    # @brief List containing all ${model.plural}.
    ${lowercase(model.plural)} = []

%   endif
% endfor

% for datum in globals:
    #\
    # @fn get_${datum.name}
    #  @breif Accessor function for ${datum.name}
    def get_${datum.name}(self):
        return self.${datum.name}

% endfor

