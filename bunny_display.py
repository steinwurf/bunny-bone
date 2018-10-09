#!/usr/bin/python
import curses
import time
import threading
import datetime
import logging

READING_INTERVAL_SEC = 15

threadLock = threading.Lock()
class Display(object):

    def __init__(self, aliases):
        self.devices = {}
        for alias in aliases:
            self.devices[alias] = {'results': 0, 'lastResult': 0, 'lastReceived': 'never', 'lastRead': 'never', 'state': 'Disconnected', 'buffered': 'unknown'}

        self.screen = None

    def start(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.refresh()

    def handle_event(self, alias, event):
        logging.debug('Event happened: {}'.format(event))
        self.devices[alias]['state'] = event
        self.refresh()

    def handle_data(self, alias, data):

        now = datetime.datetime.now()
        send_time = datetime.timedelta(milliseconds=data['send_time'])
        read_time = datetime.timedelta(milliseconds=data["read_time"])

        device_start_time = now - send_time
        absolut_read_time = device_start_time + read_time

        buffered = int((now - absolut_read_time).total_seconds() / READING_INTERVAL_SEC)
        logging.debug('Expected data readings buffered based on a reading per {} seconds: {}'.format(READING_INTERVAL_SEC, buffered))
        self.devices[alias]['results'] += 1
        self.devices[alias]['lastReceived'] = now.strftime("%H:%M:%S")
        self.devices[alias]['lastRead'] = absolut_read_time.strftime("%H:%M:%S")
        self.devices[alias]['lastResult'] = data['value']
        self.devices[alias]['buffered'] = "~ {}".format(buffered)
        self.refresh()

    def refresh(self):
        threadLock.acquire()
        if not self.screen:
            return
        self.screen.clear()
        self.screen.addstr(0,0,"Name".ljust(7) + "Status".ljust(16) + "Reading Count".ljust(15) + "Last Value".ljust(12) + "Read".ljust(9) + "Received".ljust(11) + "Buffer Count".ljust(14) + "\n",curses.A_UNDERLINE)
        offset = 1
        for line, device in enumerate(self.devices):
            line += offset
            stats = self.devices[device]
            self.screen.addstr(line, 0, device.ljust(7) + stats['state'].ljust(16) + str(stats['results']).ljust(15) + str(stats['lastResult']).ljust(12) + stats['lastRead'].ljust(9) + stats['lastReceived'].ljust(11) + stats['buffered'].ljust(14) + "\n")

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
