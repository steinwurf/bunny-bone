#!/usr/bin/python
import curses
import time
import threading

threadLock = threading.Lock()
class Display(object):

    def __init__(self, aliases):
        self.devices = {}
        for alias in aliases:
            self.devices[alias] = {'results': 0, 'lastResult': 0, 'lastRecived': 'never', 'state': 'not seen'}

        self.screen = None

    def start(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.refresh()

    def handle_event(self, alias, event):
        self.devices[alias]['state'] = event
        self.refresh()

    def handle_data(self, alias, data):
        self.devices[alias]['results'] += 1
        self.devices[alias]['lastRecived'] = time.strftime("%H:%M:%S")
        self.devices[alias]['lastResult'] = data['value']
        self.refresh()

    def refresh(self):
        threadLock.acquire()
        if not self.screen:
            return
        self.screen.clear()
        self.screen.addstr(0,0,"Name".ljust(16) + "State".ljust(18) + "Last".ljust(10) + "Count".ljust(10) + "Last".ljust(10) + "\n",curses.A_UNDERLINE)
        offset = 1
        for line, device in enumerate(self.devices):
            line += offset
            stats = self.devices[device]
            self.screen.addstr(line, 0, device.ljust(16) + stats['state'].ljust(18) + str(stats['lastResult']).ljust(10) + str(stats['results']).ljust(10) + stats['lastRecived'].ljust(10) + "\n")

        self.screen.addstr(len(self.devices) + offset + 1, 0, "Press 'q' to quit.\n")
        self.screen.refresh()
        threadLock.release()

    def getch(self):
        if not self.screen:
            return None
        return self.screen.getch()

    def stop(self):
        threadLock.acquire()
        if not self.screen:
            return
        self.screen = None
        curses.endwin()
        print("Quitting...")
        threadLock.release()
