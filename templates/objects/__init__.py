from .game_object import GameObject
% for model in models:
from .${model.name} import ${model.name}
% endfor
