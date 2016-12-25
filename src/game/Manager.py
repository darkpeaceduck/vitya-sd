from game.gfx import Frame
import threading
import copy
from time import sleep
from game.World import World

class Manager:
    LOGIC_TICK = 0.2
    def register_keys(self):
        self.gfx.register_key_event('q', self.gfx.finit)
        
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
#             print(self.world.field()._field[0])
            self.gfx.push_frame(Frame(self.world.field(), {}))
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
        
    def start(self):
        self.logic_t.start()
        self.gfx.start_loops()
        self.gfx.join_loops()
        self.logic_t.join()
    

