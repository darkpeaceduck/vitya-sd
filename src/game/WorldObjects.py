from game.surroundings import Grass, Wall, Surrounding
from game.characters import PlayerCharacter, IISolder
from enum import Enum

# def huy(cls):
#     if cls == Grass:
#         print("grass")
#         
#     if cls == Wall:
#         print("wall")
        
object_entities = {}
def world_obj(cls):
    class Wrapper(cls):
        def __init__(self, *args):
            cls.__init__(self, *args)
        def serialiaze(self):
            return cls.TAG
            
    object_entities[cls.TAG] = Wrapper
    return Wrapper
    
# class WorldObject:
#     def serialiaze(self):
#         pass

class ObjectProfileEnum(Enum):
    SURROUNDING = 1
    PLAYER = 2
    CHARACTER = 3
    
@world_obj
class GrassObject(Grass):
    TAG = '*'
    PROFILE = ObjectProfileEnum.SURROUNDING
    

@world_obj    
class WallObject(Wall):
    TAG = '#'
    PROFILE = ObjectProfileEnum.SURROUNDING

@world_obj
class PlayerCharacterObject(PlayerCharacter):
    TAG = 'P'
    PROFILE = ObjectProfileEnum.PLAYER

@world_obj
class IISolderObject(IISolder):
    TAG = 'S'
    PROFILE = ObjectProfileEnum.CHARACTER
    
def deserialiaze(chr):
    return object_entities[chr]

# print(object_entities)
# print(GrassObject().serialiaze())
# print(WallObject().serialiaze())
# print(deserialiaze('*').serialiaze())
# def     
# huy(Grass)
# huy(Wall)