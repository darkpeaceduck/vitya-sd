from game.WorldObjects import deserialiaze, ObjectProfileEnum, GrassObject
from game.field import Field
from game.logic import simulate_fight
class World:
    def __init__(self, field):
        self.locations = {}
        self.objcts = []
        self.surroundings = []
        self.player = None
        self.game_over = False
        
        self.rows, self.cols = field.get_demensions()
        for x in range(self.rows):
            for y in range(self.cols):
                cls = deserialiaze(field.get_at(x, y))
                obj = cls()
                self.set_location(obj, (x, y))
                grass_obj = GrassObject()
                self.set_location(grass_obj, (x,y))
                #low priority
                self.surroundings.append(grass_obj)
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
        print(new_location)
        if not self.out_of_bounds(new_location) and not self.obstruction_at(new_location):
            self.set_location(obj, new_location) 
        
    def objects(self):
        return self.objcts
    
    def player_location(self):
        return self.location(self.player)
    
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
    
    def set_game_over(self):
        self.game_over = True
        
    def is_game_over(self):
        return self.game_over 
    
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
                    self.set_game_over()
                    return
                self.player = winner
                destroyed.append(obj)
                
        for obj in destroyed:
            self.destroy_obj(obj)
                
        
                
#     def new_weapon(self, weapon, center, vec):
#         pass
    
    