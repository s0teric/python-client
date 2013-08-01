# -*- python -*-

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
  def __init__(self\
% for datum in model.data:
, ${datum.name}\
% endfor
):
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
    pass
%   endfor

  #MODEL DATUM ACCESSORS
%   for datum in model.data:
  #${datum.name}
  #${datum.doc}
  def get_${datum.name}(self):
    return ${datum.name}
%   endfor


% endfor