from game.gfx import Frame
import threading
import copy
from time import sleep
from game.World import World

class Manager:
    LOGIC_TICK = 0.2
    def register_keys(self):
        self.gfx.register_key_event('Q', self.gfx.finit)
        
    def register_events(self):
        self.gfx.set_on_finit(self.on_finit)
        
    def next_world(self):
        pass
#         next_world = copy.copy(self.world)
#         next_actions = []
#         for obj in next_world.objcts():
#             next_actions.append(obj.make_action(obj, self.world))
#         next_world.changes(next_actions)
#         self.world = next_world
                
    def logic_thread(self):
        self.world = World(self.start_field)
        while not self.finit:
            self.next_world()
            self.gfx.push_frame(Frame(self.world.frame(), {}))
            sleep(self.LOGIC_TICK)
                
            
    def __init__(self, field, gfx):
        self.finit = False
        self.gfx = gfx
        self.start_field = field
        self.register_keys()
        self.register_events()
        
    def on_finit(self):
        self.finit = True
        
    def start(self):
        self.logic_t = threading.Thread(target=self.logic_thread)
        self.gfx.start_loops()
        self.gfx.join_loops()
    

