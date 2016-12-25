from game.actions import *
import random
import math

def choose_closest(v, v2):
    x, y = v
    x2, y2 = v2
    if min(abs(x-x2), abs(y-y2)) == 0: 
        return (0, 0)
    if abs(x-x2) < abs(y-y2):
        return (int((x-x2)/abs(x-x2)), 0)
    else:
        return (0, int((y-y2)/ abs(y-y2)))

def choose_farest(v, v2):
    x, y = v
    x2, y2 = v2
    if abs(x-x2) < abs(y-y2):
        vec = (0, int((y-y2)/ abs(y-y2)))
    else:
        vec = (int((x-x2)/abs(x-x2)), 0)
    return vec

#strategy
class Maker:
    def make_action(self, obj, world):
        return Action()
    
class MoveGreedyStrat(Maker):
    _move_order = [LEFT, UP, RIGHT, DOWN]
    _index = 0
    def make_action(self, obj, world):
        x, y = world.location(obj)
        for _ in range(len(self._move_order)):
            vec_x, vec_y = self._move_order[self._index]
            to_x, to_y = x + vec_x, y + vec_y
            if not world.obstruction_at((to_x, to_y)) and \
            not world.out_of_bounds((to_x,to_y)):
                return MoveAction(obj, world, (vec_x, vec_y))
            else:
                self._index = (self._index + 1) % len(self._move_order)
        return Action()
      
class MoveToPlayerMaker(Maker):
    def make_action(self, obj, world):
        v = world.player_location()
        v2 = world.location(obj)
        if v == v2:
            return Action()
        vec_x, vec_y = choose_farest(v, v2)
        v_x, v_y = v2
        to_x, to_y =  v_x + vec_x, v_y + vec_y
        if world.obstruction_at((to_x, to_y)):
            vec_x, vec_y = choose_closest(v, v2)
        return MoveAction(obj, world, (vec_x, vec_y))
    
class MoveToVectorMake(Maker):
    def __init__(self, vec):
        self.vec = vec
    def make_action(self, obj, world):
        v_x, v_y = world.location(obj)
        x, y = self.vec
        to_x, to_y = v_x + x, v_y + y
        if world.out_of_bounds((to_x, to_y)) or world.obstruction_at((to_x, to_y)):
            return DestroyAction(obj)
        return MoveAction(obj, world, self.vec)

class ThrowWeaponToPlayerMaker(ThrowAction):
    def __init__(self, wp_cls):
        self.wp_cls = wp_cls
    def make_action(self, obj, world):
        v = world.player_location()
        v2 = world.location(obj)
        if v == v2:
            return Action()
        vec = choose_farest(v, v2)
        return ThrowAction(obj, self.wp_cls(vec), world)


#composite
class StratComposite(Action):
    def __init__(self):
        self.sts = []
    def add_strat(self, strat, priority):
        self.sts.append([strat, 0, priority])
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
    def make_action(self, obj, world):
        self.next_iter()
        strat = self.choose_strat()
        print(strat) 
        print(type(strat).__name__)
        return strat.make_action(obj, world)