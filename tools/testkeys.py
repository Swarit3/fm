import curses

def main(stdscr):
    stdscr.keypad(True)
    stdscr.nodelay(True)
    store = 369
    scrnY, scrnX = stdscr.getmaxyx()
    while True:
        key = stdscr.getch()

        if key != -1:
           store = key
        stdscr.addstr(0, 0, str(store) + "   :   " + chr(store))
        stdscr.addstr(1, 0, str(scrnY) + "  " + str(scrnX))

        stdscr.refresh()

curses.wrapper(main)
