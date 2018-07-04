#!/usr/bin/python
import curses
import datetime
import os
import threading
import time

class CSVResultWriter(object):

    def __init__(self, output_files):
        self.output_files = output_files

    def handle_data(self, alias, data):
        output_file = os.path.expanduser(self.output_files[alias])
        with open(output_file, 'a') as f:
            if f.tell() == 0:
                f.write('Time,Reading\n')

            send_time = datetime.timedelta(milliseconds=data['send_time'])
            read_time = datetime.timedelta(milliseconds=data["read_time"])

            device_start_time = datetime.datetime.now() - send_time
            absolut_read_time = device_start_time + read_time

            f.write('{},{}\n'.format(
                absolut_read_time.strftime("%Y-%m-%d %H:%M:%S"),
                data["value"]
            ))
