from game.gfx import Frame
import threading
import copy
from time import sleep
from game.World import World

class Manager:
    LOGIC_TICK = 0.2
    def register_keys(self):
        self.gfx.register_key_event('q', self.game_over)
        
    def register_events(self):
        self.gfx.set_on_finit(self.on_finit)
        
    def next_world(self):
        next_world = copy.copy(self.world)
        next_actions = self.world.produce_step_actions(self.LOGIC_TICK)
        next_world.impact(next_actions)
        self.world = next_world
                
    def logic_thread(self):
        self.world = World(self.start_field)
        while not self.finit:
            self.next_world()
#             field = self.world.field()
#             for row in range(field._rows):
#                 print(field._field[row])
#             print(self.world.field()._field[0])
            self.gfx.push_frame(Frame(self.world.field(), self.world.player_status()))
            if self.world.is_game_over():
                self.game_over()
            sleep(self.LOGIC_TICK)
                
            
    def __init__(self, field, gfx):
        self.finit = False
        self.start_field = field
        self.gfx = gfx
        self.register_keys()
        self.register_events()
        self.logic_t = threading.Thread(target=self.logic_thread)
        
    def on_finit(self):
        self.finit = True
        
    def game_over(self):
        self.finit = True
        self.gfx.finit()
        
    def start(self):
        self.logic_t.start()
        self.gfx.start_loops()
        self.gfx.join_loops()
        self.logic_t.join()
    

