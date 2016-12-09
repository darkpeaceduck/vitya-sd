from game.util import Singleton
from game.action_makers import MoveToPlayerMaker, Maker,\
    ThrowWeaponToPlayerMaker, StratComposite, MoveGreedyStrat

#builder
class CharacteristicsBuilder:
    def start_build(self, character):
        self.character = character
        
    def start_hp(self):
        self.character.hp = 200
    
    def start_armor(self):
        self.character.armor = 0
    
    def start_speed(self):
        self.character.speed = 1
        
    def start_move_speed(self):
        self.character.move_speed = 1
    
    def start_damage(self):
        self.character.damage = 10
        
    def start_strategy(self):
        self.character.maker = Maker()
    
    def build(self, entity):
        self.start_build(entity)
        self.start_hp()
        self.start_armor()
        self.start_speed()
        self.start_damage()
        self.start_strategy()
        self.start_move_speed()
        return self.character
    
    
class SoilderBuilder(CharacteristicsBuilder):
    def start_armor(self):
        self.character.armor = 50
    def start_damage(self):
        self.character.damage = 100
    def start_move_speed(self):
        self.character.move_speed = 2
        
class LightSoilderBuilder(CharacteristicsBuilder):
    def start_hp(self):
        self.character.hp = 200
    def start_armor(self):
        self.character.armor = 0
    def start_damage(self):
        self.character.damage = 50
    def move_speed(self):
        self.character.move_speed = 3

class IIBuiler(CharacteristicsBuilder):
    def start_strategy(self):
        self.character.maker = MoveToPlayerMaker()
     
#+singleton   
class IISolderBuilder(Singleton, IIBuiler, SoilderBuilder):
    def start_strategy(self):
        IIBuiler.start_strategy(self)

class IIArcherBuilder(LightSoilderBuilder):
    def __init__(self, wp):
        self.wp = wp
    def start_strategy(self):
        self.character.maker = StratComposite()
        self.character.maker.add_strat(MoveGreedyStrat(), 1)
        self.character.maker.add_strat(ThrowWeaponToPlayerMaker(self.wp), 0)
    
        
class Character(Maker):
    def __init__(self):
        self.builder().build(self)
    #factory method
    def builder(self):
        return CharacteristicsBuilder()
    
    def make_action(self, obj, world):
        return self.maker.make_action(obj, world)
    
    
class IISolder(Character):
    def __init__(self):
        Character.__init__(self)
        
    def builder(self):
        return IISolderBuilder()
    
class IIArcher(Character):
    def __init__(self, wp):
        self.wp = wp
        Character.__init__(self)
         
    def builder(self):
        return IIArcherBuilder(self.wp)
    
class PlayerCharacter(Character):
    def __init__(self, cls):
        self.cls = cls
        Character.__init__(self)
        
    def builder(self):
        return self.cls()
    
        
    
    
        
