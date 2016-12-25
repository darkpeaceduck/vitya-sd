from game.action_makers import MoveToVectorMake
class Item:
    move_speed = 0
    peed = 0
    damage = 0
    armor = 0
    hp = 0
    active = 0
    owner = None
    
class KnifeDrop(Item):
    move_speed = 4
    damage = 200
    speed = 3
    hp = 100
    active = 1
    
class Sword(Item):
    damage = 300
    
class Shield(Item):
    armor = 300
    
class KnifeActive(KnifeDrop, MoveToVectorMake):
    def __init__(self, vec):
        MoveToVectorMake.__init__(self, vec)
    
    
    