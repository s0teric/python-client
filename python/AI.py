########## GameObjects.py ##########

% for model in models

#\
#${model.doc}
%    if model.parent:
class ${model.name}(${model.parent.name}):
%    else:
class ${model.name}(GameObject):
%    endif

%    for datum in model.data:
  def get${capitalize(datum.name)}(self):
    return

%    endfor