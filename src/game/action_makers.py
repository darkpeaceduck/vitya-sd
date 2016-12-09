from game.actions import *
import random
import math

def choose_closest(v, v2):
    x, y = v
    x2, y2 = v2
    if min(abs(x-x2), abs(y-y2)) == 0: 
        return (0, 0)
    if abs(x-x2) < abs(y-y2):
        return ((x-x2)/abs(x-x2), 0)
    else:
        return (0, (y-y2)/ abs(y-y2))

def choose_farest(v, v2):
    x, y = v
    x2, y2 = v2
    if abs(x-x2) < abs(y-y2):
        vec = (0, (y-y2)/ abs(y-y2))
    else:
        vec = ((x-x2)/abs(x-x2), 0)

#strategy
# class MoveGreedyStrat(MoveAction):
#     _move_order = [LEFT, UP, RIGHT, DOWN]
#     def __init__(self):
#         self._index = 0
#     def action(self, world):
#         for _ in range(len(self._move_order)):
#             vec = self._move_order[self._index]
#             if self.move(world, vec):
#                 return True
#             else:
#                 self._index = (self._index + 1) % len(self._move_order)
#         return False
    
class MoveToPlayerMaker:
    def make_action(self, obj, world):
        v = world.player_location()
        v2 = world.location(self)
        if v == v2:
            return Action()
        vec = choose_farest(v, v2)
        return MoveAction(obj, world, vec)
            
                
class ThrowWeaponToPlayerMaker(ThrowAction):
    def make_action(self, obj, world):
        v = world.player_location()
        v2 = world.location(self)
        if v == v2:
            return False
        vec = choose_farest(v, v2)
        return ThrowAction(obj, world, vec)
    
class PlayerMaker(ThrowAction, MoveAction):
    def make_action(self, _, world):
        if world.player_
        return world.next_player_action()
            
    
# class BlockedMagicDirectedToPlayerStrat(Action):
#     def action(self, world):
#         v = world.player_location()
#         v2 = world.location(self)
#         if v == v2:
#             return False
#         vec = choose_closest(v, v2)
#         if vec == (0, 0):
#             return False
#         return self.magic_directed(world, self.magic, vec)
#     
# class FightMagicDirectedToPlayerStrat(Action):
#     def action(self, world):
#         v = world.player_location()
#         v2 = world.location(self)
#         if v == v2:
#             return False
#         vec = choose_farest(v, v2)
#         return self.magic_directed(world, self.magic, vec)
#     
# class MagicRangedToPlayerStrat(Action):
#     pass

#composite
class StratComposite(Action):
    def __init__(self):
        self.sts = []
    def add_strat(self, strat, priority):
        self.sts.append((strat, 0, priority))
    def next_iter(self):
        for item in self.sts:
            item[1] -= 1
            if item[1] < 0:
                item[1] = item[2]
    def choose_strat(self):
        max_priority = -1
        strat = None
        for item in self.sts:
            if item[1] == 0 and max_priority < item[2]: 
                strat = item[0]
                max_priority = item[2]
        return strat
    def action(self, world):
        self.next_iter()
        self.choose_strat().action(world)
        
