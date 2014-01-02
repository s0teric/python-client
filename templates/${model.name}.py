<%
    rerun_for('model', models)
%>import operator
import utility
import json
import client_json
import json
import game
from game_object import GameObject
% if model.parent:
from ${model.parent.name} import ${model.parent.name}
% endif

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
        self._connection = connection
        self._parent_game = parent_game
##
## S 2 FOR DATA IN MODEL
% for datum in model.data:
        self._${datum.name} = ${datum.name}
% endfor
## E 2 FOR DATA IN MODEL
##

##
## S 2 FOR FUNC IN FUNCTIONS -------------------------------------------------------------------------------- func
## ------------------------------------------------------------------ model.$(func.name}(${func.args})
%   for func in model.functions:
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

        utility.send_string(self._connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self._connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self._parent_game.update_game(message)

        return status
% endfor
## E 2 FOR FUNC IN FUNCTIONS -------------------------------------------------------------------------------- func
##

##
## S 2 FOR LOCALS IN LOCALS
% for local in model.locals:
    ##Through data type
    @property
    def ${local.name}(self):
        return self._${local.name}
% endfor
## E 2 FOR LOCALS IN LOCALS


## S 2 FOR REMOTES IN REMOTES
% for remote in model.remotes:
    ##Primitive data type
    @property
    def ${remote.name}(self):
        return self.${remote.through}.${remote.name}
% endfor
## E 2 FOR REMOTES IN REMOTES
##

##
## S 2 FOR RELATION IN RELATIONS
% for relation in model.relations:
    ## Return the model with relation_id in the list of models
    @property
    def ${relation.name}(self):
        return parent_game.ai.${lowercase(relation.type.plural)}.find(self.${relation.name}_id, key=operator.attrgetter("id"))
% endfor
## E 2 FOR RELATION IN RELATIONS
##

