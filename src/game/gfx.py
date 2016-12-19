from game.field import Field
from time import sleep
import threading
import curses

class ScreenRenderer:
    def set_scr(self, stdscr):
        self._stdscr = stdscr

class FieldRenderer(ScreenRenderer):
    def render_field(self, field):
        rows, cols = field.get_demensions()
        scr = self._stdscr
        scr.clear()
        for i in range(rows):
            for j in range(cols):
                scr.addch(j, i, field.get_at(i, j))
        scr.refresh()
        
class StatusRenderer(ScreenRenderer):
    def render_stat(self, status_dict):
        self._stdscr.clear()
        for k, v in status_dict.items():
            self._stdscr.addstr(k + " : " + v + "\n")
        self._stdscr.refresh()
                
class FrameQRenderer:
    def set_renderers(self, field_renderer, status_renderer):
        self.field_renderer = field_renderer
        self.status_renderer = status_renderer
        
    def push_frame(self, frame):
        self.render_q.append(frame)
             
    def render_frame(self, frame):
        self.field_renderer.render_field(frame.field)   
        self.status_renderer.render_stat(frame.stat)
        
                
class Gfx(FrameQRenderer, ScreenRenderer):
    RENDER_TICK = 0.01
    def __init__(self):
        #default atomic pusher/getter
        self.render_q = []
        #atomic flag
        self.finilizated = False
        
    def update_input_derwin(self):
        self._stdscr.clear()
        self._stdscr.refresh()
    
    def render_loop(self):
        while not self.finilizated:
            if len(self.render_q) > 0:
                frame = self.render_q.pop()
                self.render_frame(frame)
                
            self.update_input_derwin()
            sleep(self.RENDER_TICK)
            
    def io_loop(self):
        while 1:
            event = self._stdscr.getch()
            if (event == ord('Q')):
                break
        self.finilizated = True
        
    def start_loops(self):
        self.render_t = threading.Thread(target=self.render_loop)
        self.io_t = threading.Thread(target=self.io_loop)
        self.render_t.start()
        self.io_t.start()
        
    def join_loops(self):
        self.render_t.join()
        self.io_t.join()
        
class Frame:
    def __init__(self, field, stat):
        self.field = field
        self.stat = stat
        
    
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

a = Field(2, 2)
a.set_at(0, 0, 'H')
a.set_at(1, 1, 'P')
stat = {}
fieldr = FieldRenderer()
gfx = Gfx()
statusr = StatusRenderer()

sc = curses.initscr()
fieldr.set_scr(sc.derwin(0, 0))
statusr.set_scr(sc.derwin(5, 0))
gfx.set_scr(sc.derwin(11, 0))

gfx.set_renderers(fieldr, statusr)
frame = Frame(a, stat)
gfx.push_frame(frame)

gfx.start_loops()

for i in range(ord('A'), ord('Z')):
    a.set_at(0, 1, chr(i))
    stat["pizda"] = "huy" + chr(i)
    gfx.push_frame(frame)
    sleep(1)
gfx.join_loops()

curses.endwin()


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