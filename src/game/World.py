from game.WorldObjects import deserialiaze, ObjectProfileEnum
from game.field import Field
class World:
    def __init__(self, field):
        self.locations = {}
        self.objcts = []
        self.surroundings = []
        self.player = None
        
        self.rows, self.cols = field.get_demensions()
        for x in range(self.rows):
            for y in range(self.cols):
                cls = deserialiaze(field.get_at(x, y))
                obj = cls()
                self.new_location(obj, x, y)
                if cls.PROFILE == ObjectProfileEnum.PLAYER:
                    self.player = obj
                if cls.PROFILE == ObjectProfileEnum.CHARACTER:
                    self.objcts.append(obj)
                if cls.PROFILE == ObjectProfileEnum.SURROUNDING:
                    self.surroundings.append(obj)
        
    def new_location(self, obj, new_location):
        self.locations[obj]= new_location
        
    def location(self, obj):
        return self.locations[obj]
        
    def objcts(self):
        return self.objcts
    
    def field(self):
        field = Field(self.rows, self.cols)
        def dump_list(list):
            for item in list:
                x, y = self.location(item)
                field.set_at(x, y, item.serialiaze())
        dump_list(self.objcts)
        dump_list(self.surroundings)
        dump_list([self.player])
        return field
                
#     def new_weapon(self, weapon, center, vec):
#         pass
    
    