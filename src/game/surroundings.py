from game.util import Singleton

#builder + singleton
class SurroundingsBuilder(Singleton):
    def start_build(self, entity):
        self.entity = entity
        
    def start_destroyable(self):
        self.entity.destroyable = False
        
    def start_strength(self):
        self.entity.strength = -1
        
    def start_obstruction(self):
        self.entity.obstruction = False
        
    def build(self, entity):
        self.start_build(entity)
        self.start_destroyable()
        self.start_strength()
        self.start_obstruction()
        return self.entity
    
class WallBuilder(SurroundingsBuilder):
    def start_destroyable(self):
        self.entity.destroyable = True
        
    def start_strength(self):
        self.entity.strength = 3000
        
    def start_obstruction(self):
        self.entity.obstruction = True 

class Surrounding:
    def __init__(self):
        self.builder().build(self)
    #factory method
    def builder(self):
        return SurroundingsBuilder()
    
class Wall(Surrounding):
    def __init__(self):
        Surrounding.__init__(self)    
        
    def builder(self):
        return WallBuilder()
    
class Grass(Surrounding):
    def __init__(self):
        Surrounding.__init__(self)