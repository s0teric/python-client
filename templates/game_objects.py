# -*- python -*-

import utility
import json
import client_json

class GameObject():
    def __init__(self):
        pass

% for model in models:

#${model.name}
#${model.doc}
% if model.parent:
class ${model.name}(${model.parent.name}):
% else:
class ${model.name}(GameObject):
% endif

    #INIT
    def __init__(self, connection, parent_game\
% for datum in model.data:
, ${datum.name}\
% endfor
):
        self.connection = connection
        self.parent_game = parent_game
% for datum in model.data:
        self.${datum.name} = ${datum.name}
% endfor

    #MODEL FUNCTIONS
%   for func in model.functions + model.properties:
    #${func.name}
    #${func.doc}
    def ${func.name}(self\
% for args in func.arguments:
, ${args.name}\
% endfor
):
        function_call = client_json.function_call.copy()
        function_call.update({"type": ${repr(func.name)}})
        function_call.get("args").update({"actor": self.id})

% for args in func.arguments:
        function_call.get("args").update({${repr(args.name)}: repr(${args.name})})
% endfor

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
%   endfor

    #MODEL DATUM ACCESSORS
%   for datum in model.data:
    #${datum.name}
    #${datum.doc}
    def get_${datum.name}(self):
        return ${datum.name}
%   endfor


% endfor
