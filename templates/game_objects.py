# -*- python -*-

import utility
import json
import client_json


class GameObject():
    def __init__(self):
        pass

##
## S 1 FOR MODEL IN MODELS ---------------------------------------------------------------------------------- model
% for model in models:

#\
# @class ${model.name}
% if model.doc:
#  @brief ${model.doc}
% endif
## ------------------------------------------------------------------ model.parent
% if model.parent:
class ${model.name}(${model.parent.name}):
% else:
class ${model.name}(GameObject):
% endif

## ------------------------------------------------------------------ model.__init__()
    def __init__(self, connection, parent_game\
## S 2 FOR DATA IN MODEL
% for datum in model.data:
, ${datum.name}\
% endfor
):
## E 2 FOR DATA IN MODEL
##
        self.connection = connection
        self.parent_game = parent_game
##
## S 2 FOR DATA IN MODEL
% for datum in model.data:
        self.${datum.name} = ${datum.name}
% endfor
## E 2 FOR DATA IN MODEL
##

##
## S 2 FOR FUNC IN FUNCTIONS -------------------------------------------------------------------------------- func
## ------------------------------------------------------------------ model.$(func.name}(${func.args})
%   for func in model.functions + model.properties:
    #\
# @fn ${func.name}
% if func.doc:
    #  @brief ${func.doc}
% endif
##
## S 3 FOR ARGS IN FUNC
% for args in func.arguments:
% if args.doc:
    #  @param ${args.name} ${args.doc}
% endif
% endfor
## E 3 FOR ARGS IN FUNC
##
    def ${func.name}(self\
## S 3 FOR ARGS IN FUNC
% for args in func.arguments:
, ${args.name}\
% endfor
## E 3 FOR ARGS IN FUNC
##
):
        function_call = client_json.function_call.copy()
        function_call.update({"type": ${repr(func.name)}})
        function_call.get("args").update({"actor": self.id})
##
## S 3 FOR ARGS IN FUNC
% for args in func.arguments:
        function_call.get("args").update({${repr(args.name)}: repr(${args.name})})
% endfor
## E 3 FOR ARGS IN FUNC
##

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status
% endfor
## E 2 FOR FUNC IN FUNCTIONS -------------------------------------------------------------------------------- func
##

##
## S 2 FOR DATUM IN DATA ------------------------------------------------------------------------------------ datum
## ------------------------------------------------------------------ model.get_${datum.name}()
% for datum in model.data:
% if datum.through:
    #\
#  @fn get_${datum.name}
    #  @brief Accessor function for ${datum.name} through ${datum.through}
    def get_${datum.name}(self):
        if self.${through}
        return self.${through}.${datum.name}
% else:
    #\
#  @fn get_${datum.name}
    #  @brief Accessor function for ${datum.name}
    def get_${datum.name}(self):
        return self.${datum.name}
% endif

% endfor
## E 2 FOR DATUM IN DATA ------------------------------------------------------------------------------------ datum
##
% endfor
## E 1 FOR MODEL IN MODELS ---------------------------------------------------------------------------------- model
##
