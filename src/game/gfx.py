from game.field import Field
from time import sleep
import threading
import curses
import copy

class ScreenRenderer:
    def set_scr(self, stdscr):
        self._stdscr = stdscr
        
    def get_scr(self):
        return self._stdscr

class FieldRenderer(ScreenRenderer):
    def render_field(self, field):
        rows, cols = field.get_demensions()
        scr = self.get_scr()
        scr.clear()
        for i in range(rows):
            for j in range(cols):
                scr.addch(i, j, field.get_at(i, j))
        scr.refresh()
        
class StatusRenderer(ScreenRenderer):
    def render_stat(self, status_dict):
        self.get_scr().clear()
        for k, v in status_dict.items():
            self.get_scr().addstr(k + " : " + v + "\n")
        self.get_scr().refresh()
                
class FrameQRenderer:
    def __init__(self):
        self.render_q = []
    def set_renderers(self, field_renderer, status_renderer):
        self.field_renderer = field_renderer
        self.status_renderer = status_renderer
        
    def push_frame(self, frame):
        self.render_q.append(frame)
             
    def render_frame(self, frame):
        self.field_renderer.render_field(frame.field)   
        self.status_renderer.render_stat(frame.stat)
        
class IOControllerRenderer(ScreenRenderer):
    NON_BLOCKING_IO_DELAY_TIMEOUT = 0.001
    def __init__(self):
        self.finilizated = False
        self.key_ev_list = {}
    def update_input_derwin(self):
        self._stdscr.clear()
        self._stdscr.refresh()
    
    def invoke_event(self, event):
        event()
        
    def set_on_finit(self, event):
        self.on_finit = event
        
    def io_loop(self):
        self.get_scr().nodelay(True)
        while not self.is_finilizated():
            event = self._stdscr.getch()
            if event in self.key_ev_list:
                self.invoke_event(self.key_ev_list[event])
            sleep(self.NON_BLOCKING_IO_DELAY_TIMEOUT)
        self.finit()
        
    def is_finilizated(self):
        return self.finilizated
    
    def finit(self):
        self.finilizated = True
        self.invoke_event(self.on_finit)
        
    def register_key_event(self, key, event):
        self.key_ev_list[ord(key)] = event
        
                
class Gfx(FrameQRenderer, IOControllerRenderer):
    RENDER_TICK = 0.001
    def __init__(self):
        FrameQRenderer.__init__(self)
        IOControllerRenderer.__init__(self)
    
    def render_loop(self):
        while not self.finilizated:
            if len(self.render_q) > 0:
                frame = self.render_q.pop()
                self.render_frame(frame)
                
            self.update_input_derwin()
            sleep(self.RENDER_TICK)
            
        
    def start_loops(self):
        self.render_t = threading.Thread(target=self.render_loop)
        self.io_t = threading.Thread(target=self.io_loop)
        self.render_t.start()
        self.io_t.start()
        
    def join_loops(self):
        self.render_t.join()
        self.io_t.join()
        curses.endwin()    
        
class GfxDefault(Gfx):
    FIELD_PROPORTION = 5
    STATUS_PROPORTION = 3
    IO_PROPORTION = 1
    def __init__(self):
        Gfx.__init__(self)
        sc = curses.initscr()
        fieldr = FieldRenderer()
        statusr = StatusRenderer()
        
        h, _ = sc.getmaxyx()
        fieldr.set_scr(sc.derwin(0, 0))
        parts = (self.FIELD_PROPORTION + self.STATUS_PROPORTION + self.IO_PROPORTION) 
        statusr.set_scr(sc.derwin(int(1.0 * self.FIELD_PROPORTION / parts * h) , 0))
        self.set_scr(sc.derwin(int(1.0 * (self.FIELD_PROPORTION + self.STATUS_PROPORTION) / parts * h), 0))
        self.set_renderers(fieldr, statusr)
        
class Frame:
    def __init__(self, field, stat):
        self.field = copy.copy(field)
        self.stat = copy.copy(stat)
        
    
# def update(fi, field):
#     va = 0
#     scr = fi._stdscr
#     while not fi.stopped:
#     #         scr.clear()
#         fi.render_field(field)
#         if va % 2 == 0:
#             field.set_at(0, 0, 'A')
#         else:
#             field.set_at(0, 0, 'B')
#         scr.refresh()
#         va += 1
#         sleep(0.1)
#         
# class Controls(ScreenRenderer):
#     def render(self, field):
#         scr = self._stdscr
#         scr.addstr(0, 0, "USER INPUT")
# 
# import curses
# import threading

# a = Field(2, 2)
# a.set_at(0, 0, 'H')
# a.set_at(1, 1, 'P')
# stat = {}
# 
# gfx = GfxDefault()
# gfx.push_frame(Frame(a, stat))
# gfx.register_key_event('Q', gfx.finit)
# 
# gfx.start_loops()
# 
# for i in range(ord('A'), ord('Z')):
#     a.set_at(0, 1, chr(i))
#     stat["pizda"] = "huy" + chr(i)
#     gfx.push_frame(Frame(a, stat))
#     if gfx.is_finilizated():
#         break
#     sleep(1)
# 
# gfx.join_loops()


# 
# fi = FieldRenderer()
# co = Controls()
# fi.set_scr(scr.derwin(0, 0))
# derscr = scr.derwin(11, 0)
# co.set_scr(derscr)
# 
# fi.stopped = False
# derscr.clear()
# co.render(a)
# clock = threading.Thread(target=update, args=(fi, a))
# clock.start()
# while 1:
#     event = derscr.getch()
#     if event == ord("q"):
#         fi.stopped = True
#         break
#     if event == ord("d"):
#         derscr.clear()
#         co.render(a)
# curses.endwin()