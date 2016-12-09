from game.util import Singleton
from game.strategies import MoveToPlayerMaker, StratComposite,\
    ThrowWeaponToPlayerMaker, MoveGreedyStrat
#builder + singleton
class CharacteristicsBuilder(Singleton):
    def start_build(self, character):
        self.character = character
        
    def start_hp(self):
        self.character.hp = 200
    
    def start_armor(self):
        self.character.armor = 0
    
    def start_speed(self):
        self.character.speed = 1
    
    def start_damage(self):
        self.character.damage = 10
        
#     def start_magic(self):
#         self.character.magic = 0
    
    def build(self, character):
        self.start_build(character)
        self.build_internal()
        self.start_hp()
        self.start_armor()
        self.start_speed()
        self.start_damage()
#         self.start_magic()
        return self.character
    
    def incremental_build(self, character):
        return self.build()
    
class SoilderBuilder(CharacteristicsBuilder):
    def start_armor(self):
        self.character.armor = 50
    def start_damage(self):
        self.character.damage = 100
    def start_speed(self):
        self.speed = 2
        
class HeavySoilderBuilder(CharacteristicsBuilder):
    def start_hp(self):
        self.character.hp = 300
    def start_armor(self):
        self.character.armor = 100
    def start_damage(self):
        self.character.damage = 200
        
class ArcherBuilder(CharacteristicsBuilder):
    def start_range_weapon(self):
        self.range_weapon = None
    def incremental_build(self, character):
        self.start_range_weapon()
        return self.character
    def build(self, character):
        CharacteristicsBuilder.build(self, character)
        return self.character
        
class IIBuiler(CharacteristicsBuilder):
    def start_strat(self):
        self.character.strat = MoveGreedyStrat()
    def build(self, character):
        CharacteristicsBuilder.build(self, character)
        self.start_strat()
        return self.character
        
class IISolderBuilder(IIBuiler, SoilderBuilder):
    def start_strat(self):
        self.strat = MoveToPlayerMaker()
        
class IIArcherBuilder(IIBuiler, ArcherBuilder, SoilderBuilder):
    def start_strat(self):
        self.strat = StratComposite()
        self.strat.add_strat(MoveToPlayerMaker(), 0)
        self.strat.add_strat(ThrowWeaponToPlayerMaker(), 2)
    
        
# class MageBuilder(CharacteristicsBuilder):
#     def start_armor(self):
#         self.character.armor = 10
#     def start_magic(self):
#         self.character.magic = 10
#     
class Character:
    def __init__(self):
        self.builder().build(self)
    #factory method
    def builder(self):
        return CharacteristicsBuilder()
    
class IISolder(Character):
    def __init__(self):
        Character.__init__(self)
        
    def builder(self):
        return IISolderBuilder()
    
class IIArcher(Character):
    def __init__(self):
        Character.__init__(self)
        
    def builder(self):
        return IIArcherBuilder()
    
class PlayerCharacter(Character):
    def __init__(self, cls):
        self.cls = cls
        Character.__init__(self)
        
    def builder(self):
        return self.cls()
    
        
    
    
        
