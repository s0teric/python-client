# -*- python -*-

import Utility
from AI import *
import json
import ClientJSON

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
    def __init__(self, connection\
% for datum in model.data:
, ${datum.name}\
% endfor
):
        self.connection = connection
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
        function_call = ClientJSON.function_call.copy()
        function_call.update({"type": ${repr(func.name)}})
        function_call.get("args").update({"actor": self.id})

% for args in func.arguments:
        function_call.get("args").update({${repr(args.name)}: repr(${args.name})})
% endfor
        try:
            Utility.NetworkSendString(self.connection, json.dumps(function_call))
        except:
            print("CLIENT: Failed to send command ${func.name}.")

        try:
            message = Utility.NetworkRecvString(self.connection)
        except:
            print("CLIENT: Failed to receive status after command ${func.name}.")

        return True
%   endfor

    #MODEL DATUM ACCESSORS
%   for datum in model.data:
    #${datum.name}
    #${datum.doc}
    def get_${datum.name}(self):
        return ${datum.name}
%   endfor


% endfor