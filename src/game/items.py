from game.action_makers import MoveToVectorMake
class Item:
    move_speed = 0
    peed = 0
    damage = 0
    armor = 0
    hp = 0
    
class KnifeActive(Item, MoveToVectorMake):
    move_speed = 4
    damage = 200
    speed = 3
    hp = 100
    def __init__(self, vec):
        MoveToVectorMake.__init__(self, vec)
    
    