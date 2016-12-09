import curses
import time
import threading

def update_time(screen):
    while 1:
        screen.addstr(12, 12, time.strftime("%a, %d %b %Y %H:%M:%S"))
        screen.refresh()
        time.sleep(1)

screen = curses.initscr()
# curses.noecho()
curses.curs_set(0)
screen.keypad(1)

screen.addstr("This is a Sample Curses Script\n\n")
screen.refresh()

clock = threading.Thread(target=update_time, args=(screen,))
clock.daemon = True
clock.start()
while 1:
    event = screen.getch()
    if event == ord("q"):
        break

curses.endwin()