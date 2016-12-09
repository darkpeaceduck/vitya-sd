
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

class Action():
    def impact(self, world):
        pass

class MoveAction(Action):
    def impact(self, world):
        return world.new_location(self.obj, self.new_location)
    
    def __init__(self, obj, world, vec):
        self.obj = obj
        x, y = world.location(obj)
        x2, y2 = vec
        self.new_location = (x+x2, y+y2)
    
class ThrowAction(Action):
    def __init__(self, obj, world, move_vector):
        self.obj_location = world.location(obj)
        self.obj = obj
        self.move_vector = move_vector
        
    def impact(self, world):
        return world.new_weapon(self.obj.range_weapon, self.obj_location, self.move_vector)
        
# def MagicAction(Action):
#     def magic_directed(self, world, move_vector):
#         return world.new_directed_magic(magic, world.location(self), move_vector)
#     
#     def magic_range(self, world, magic):
#         return world.new_range_magic(magic, world.location(self))