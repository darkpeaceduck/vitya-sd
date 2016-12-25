from game.surroundings import Grass, Wall, Surrounding
from game.characters import PlayerCharacter, IISolder, SoilderBuilder
from game.items import *
from enum import Enum

        
object_entities = {}
def world_obj(cls):
    class Wrapper(cls):
        def __init__(self, *args):
            try:
                cls.__init__(self, *cls.INIT_PARAMS, *args)
            except AttributeError:
                cls.__init__(self, *args)
        def serialiaze(self):
            return cls.TAG
            
    object_entities[cls.TAG] = Wrapper
    return Wrapper
    

class ObjectProfileEnum(Enum):
    SURROUNDING = 1
    PLAYER = 2
    CHARACTER = 3
    ITEM = 4
    
@world_obj
class GrassObject(Grass):
    TAG = '.'
    PROFILE = ObjectProfileEnum.SURROUNDING
    

@world_obj    
class WallObject(Wall):
    TAG = '#'
    PROFILE = ObjectProfileEnum.SURROUNDING

@world_obj
class PlayerCharacterObject(PlayerCharacter):
    TAG = 'P'
    PROFILE = ObjectProfileEnum.PLAYER
    INIT_PARAMS = [SoilderBuilder]

@world_obj
class IISolderObject(IISolder):
    TAG = 'S'
    PROFILE = ObjectProfileEnum.CHARACTER

@world_obj    
class KnifeActiveObject(KnifeActive):
    TAG = '@'
    PROFILE = ObjectProfileEnum.ITEM
    
@world_obj
class KnifeDrop(KnifeDrop):
    TAG = 'K'
    PROFILE = ObjectProfileEnum.ITEM
    
def deserialiaze(chr):
    return object_entities[chr]

# print(object_entities)
# print(GrassObject().serialiaze())
# print(WallObject().serialiaze())
# print(deserialiaze('K')().serialiaze())
# def     
# huy(Grass)
# huy(Wall)