import game_objects

class ModelContainer():
    all_objects = {}

% for model in models:
    ${lowercase(model.plural)} = []
% endfor

    def add_object(self, to_add):

% for model in models:
        if isinstance(to_add, game_objects.${model.name}):
            all_objects[to_add.id] = to_add


% endfor
        return False





