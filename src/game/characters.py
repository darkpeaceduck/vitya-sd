from game.util import Singleton
from game.action_makers import MoveToPlayerMaker, Maker
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
        
    def start_strategy(self):
        self.maker = Maker()
        
#     def start_magic(self):
#         self.character.magic = 0
    
    def build(self, entity):
        self.start_build(entity)
        self.build_internal()
        self.start_hp()
        self.start_armor()
        self.start_speed()
        self.start_damage()
        self.start_strategy()
#         self.start_magic()
        return self.character
    
#     def incremental_build(self, entity):
#         return self.build()
    
class SoilderBuilder(CharacteristicsBuilder):
    def start_armor(self):
        self.character.armor = 50
    def start_damage(self):
        self.character.damage = 100
    def start_speed(self):
        self.speed = 2
        
# class HeavySoilderBuilder(CharacteristicsBuilder):
#     def start_hp(self):
#         self.character.hp = 300
#     def start_armor(self):
#         self.character.armor = 100
#     def start_damage(self):
#         self.character.damage = 200
#         
# class ArcherBuilder(CharacteristicsBuilder):
#     def start_range_weapon(self):
#         self.range_weapon = None
#     def incremental_build(self, character):
#         self.start_range_weapon()
#         return self.character
#     def build(self, character):
#         CharacteristicsBuilder.build(self, character)
#         return self.character
#         
class IIBuiler(CharacteristicsBuilder):
    def start_strategy(self):
        self.maker = MoveToPlayerMaker()
        
class IISolderBuilder(IIBuiler, SoilderBuilder):
    def start_strategy(self):
        IIBuiler.start_strategy(self)
# class IIArcherBuilder(IIBuiler, ArcherBuilder, SoilderBuilder):
#     def start_strat(self):
#         self.strat = StratComposite()
#         self.strat.add_strat(MoveToPlayerMaker(), 0)
#         self.strat.add_strat(ThrowWeaponToPlayerMaker(), 2)
    
        
# class MageBuilder(CharacteristicsBuilder):
#     def start_armor(self):
#         self.character.armor = 10
#     def start_magic(self):
#         self.character.magic = 10
#     
class Character(Maker):
    def __init__(self):
        self.builder().build(self)
    #factory method
    def builder(self):
        return CharacteristicsBuilder()
    
    def make_action(self, obj, world):
        self.maker.make_action(obj, world)
    
    
class IISolder(Character):
    def __init__(self):
        Character.__init__(self)
        
    def builder(self):
        return IISolderBuilder()
    
# class IIArcher(Character):
#     def __init__(self):
#         Character.__init__(self)
#         
#     def builder(self):
#         return IIArcherBuilder()
    
class PlayerCharacter(Character):
    def __init__(self, cls):
        self.cls = cls
        Character.__init__(self)
        
    def builder(self):
        return self.cls()
    
        
    
    
        
