# -*- python -*-

class GameObject():
  def __init__(self):
    pass

% for model in models:

#${model.doc}
% if model.parent:
class ${model.name}(${model.parent.name}):
% else:
class ${model.name}(GameObject):
% endif

%   for func in model.functions:
  def ${func.name}()
%   endfor

%   for datum in model.data:
  def get${capitalize(datum.name)}(self):
    pass
%   endfor


% endfor