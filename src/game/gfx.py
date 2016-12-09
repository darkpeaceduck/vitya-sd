from game.field import Field
from time import sleep
class ScreenRenderer:
    def set_scr(self, stdscr):
        self._stdscr = stdscr

class FieldRenderer(ScreenRenderer):
    def render_field(self, field):
        rows, cols = field.get_demensions()
        scr = self._stdscr
        for i in range(rows):
            for j in range(cols):
                scr.addch(j, i, field.get_at(i, j))
                
def update(fi, field):
    va = 0
    scr = fi._stdscr
    while not fi.stopped:
    #         scr.clear()
        fi.render_field(field)
        if va % 2 == 0:
            field.set_at(0, 0, 'A')
        else:
            field.set_at(0, 0, 'B')
        scr.refresh()
        va += 1
        sleep(0.1)
        
class Controls(ScreenRenderer):
    def render(self, field):
        scr = self._stdscr
        scr.addstr(0, 0, "USER INPUT")

import curses
import threading

a = Field(2, 2)
a.set_at(0, 0, 'H')
a.set_at(1, 1, 'P')

scr = curses.initscr()
fi = FieldRenderer()
co = Controls()
fi.set_scr(scr.derwin(0, 0))
derscr = scr.derwin(11, 0)
co.set_scr(derscr)

fi.stopped = False
derscr.clear()
co.render(a)
clock = threading.Thread(target=update, args=(fi, a))
clock.start()
while 1:
    event = derscr.getch()
    if event == ord("q"):
        fi.stopped = True
        break
    if event == ord("d"):
        derscr.clear()
        co.render(a)
curses.endwin()