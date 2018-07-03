#!/usr/bin/python
import curses
import time
import threading
import os

class CSVResultWriter(object):

    def __init__(self, output_files):
        self.output_files = output_files

    def handle_data(self, alias, data):
        output_file = os.path.expanduser(self.output_files[alias])
        with open(output_file, 'a') as f:
            if f.tell() == 0:
                f.write('Time,Reading\n')
            f.write('{},{}\n'.format(data["time"], data["value"]))
