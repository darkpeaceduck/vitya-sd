
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
        
class DestroyAction:
    def impact(self, world):
        world.destroy_obj(self.obj)
    def __init__(self, obj):
        self.obj = obj
    
class ThrowAction(Action):
    def __init__(self, obj, w_obj, world):
        self.w_obj = w_obj
        self.w_obj.owner = obj
        self.location = world.location(obj)
        
    def impact(self, world):
        return world.throw_weapon(self.w_obj, self.location)
    
# def MagicAction(Action):
#     def magic_directed(self, world, move_vector):
#         return world.new_directed_magic(magic, world.location(self), move_vector)
#     
#     def magic_range(self, world, magic):
#         return world.new_range_magic(magic, world.location(self))