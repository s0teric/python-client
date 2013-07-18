# -*- python -*-

class BaseAI():
% for model in models:
%   if model.type == "Model":
  ${lowercase(model.plural)} = []
% endfor

% for datum in globals:
  def get${capitalize(datum.name)}(self):
    pass
% endfor
