from game.WorldObjects import deserialiaze, ObjectProfileEnum, GrassObject
from game.field import Field
from game.logic import simulate_fight, can_move
from game.actions import MoveAction
from enum import Enum
class GameOver(Enum):
    NOT = 0
    WIN = 1
    LOSE = 2
class World:
    def __init__(self, field):
        self.locations = {}
        self.last_move = {}
        self.objcts = []
        self.surroundings = []
        self.player = None
        self.player_moves_q = []
        self.game_over = GameOver.NOT
        
        self.rows, self.cols = field.get_demensions()
        for x in range(self.rows):
            for y in range(self.cols):
                self.add_cls(GrassObject, (x,y))
                cls = deserialiaze(field.get_at(x, y))
                self.add_cls(cls, (x,y))
                
    def add_cls(self, cls, location):
        obj = cls()
        self.set_location(obj, location)
        self.last_move[obj] = 0.0
        if cls.PROFILE == ObjectProfileEnum.PLAYER:
            self.player = obj
        if cls.PROFILE == ObjectProfileEnum.CHARACTER:
            self.objcts.append(obj)
        if cls.PROFILE == ObjectProfileEnum.SURROUNDING:
            self.surroundings.append(obj)
        
    def set_location(self, obj, new_location):
        self.locations[obj]= new_location
        
    def location(self, obj):
        return self.locations[obj]
    
    def out_of_bounds(self, location):
        x, y = location
        return x < 0 or y < 0 or x >= self.rows or y >= self.cols
    
    def obstruction_at(self, location):
        for surr in self.surroundings:
            if surr.obstruction:
                if self.location(surr) == location:
                    return True
        return False
    
    def new_location(self, obj, new_location):
        if not self.out_of_bounds(new_location) and not self.obstruction_at(new_location):
            self.set_location(obj, new_location) 
        
    def objects(self):
        return self.objcts
    
    def player_location(self):
        return self.location(self.player)
    
    def produce_step_actions(self, delta):
        next_actions = []
        for obj in self.objects():
            new_delta = delta + self.last_move[obj]
            if can_move(obj, new_delta): 
                next_actions.append(obj.make_action(obj, self))
                new_delta = 0
            self.last_move[obj]= new_delta
        if len(self.player_moves_q) > 0:
            next_actions.append(self.player_moves_q.pop())
        return next_actions
    
    def player_moved(self, vec):
        self.player_moves_q.append(MoveAction(self.player, self, vec))
    
    def field(self):
        field = Field(self.rows, self.cols)
        def dump_list(list):
            for item in list:
                x, y = self.location(item)
                field.set_at(x, y, item.serialiaze())
        dump_list(self.surroundings)
        dump_list(self.objcts)
        dump_list([self.player])
        return field
    
    def player_status(self):
        st = {}
        st["hp"] = str(self.player.hp)
        st["armor"] = str(self.player.armor)
        st["speed"] = str(self.player.speed)
        st["damage"] = str(self.player.damage)
        return st
    
    def set_game_over(self, st):
        self.game_over = st
        
    def is_game_over(self):
        return self.game_over != GameOver.NOT
    
    def is_lose(self):
        return self.game_over == GameOver.LOSE
    
    def is_win(self):
        return self.game_over == GameOver.WIN
    
    def destroy_obj(self, obj):
        self.objcts.remove(obj)
        del self.locations[obj]
    
    def impact(self, actions):
        for action in actions:
            action.impact(self)
        destroyed = []
        for obj in self.objcts:
            if self.location(obj) == self.player_location():
                winner = simulate_fight(self.player, obj)
                if winner != self.player:
                    self.set_game_over(GameOver.LOSE)
                    return
                self.player = winner
                destroyed.append(obj)
                
        for obj in destroyed:
            self.destroy_obj(obj)
                
        
                
#     def new_weapon(self, weapon, center, vec):
#         pass
    
    