from game.util import Singleton

class SurroundingsBuilder(Singleton):
    def start_build(self, entity):
        self.entity = entity
        
    def start_destroyable(self):
        self.entity.destroyable = False
        
    def start_strength(self):
        self.strength = -1
        
    def build(self, entity):
        self.start_build(entity)
        self.start_destroyable()
        self.start_strength()
        return self.entity
    
class WallBuilder(SurroundingsBuilder):
    def start_destroyable(self):
        self.entity.destroyable = True
        
    def start_strength(self):
        self.strength = 3000

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