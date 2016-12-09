class World:
    def __init__(self):
        self.locations = {}
    def new_location(self, obj, new_location):
        self.locations[obj]= new_location
        
    def location(self, obj):
        return self.locations[obj]
        
    def new_weapon(self, weapon, center, vec):
        pass
    
    