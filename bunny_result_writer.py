#!/usr/bin/python
import curses
import time
import threading
import os
import time
import datetime

class CSVResultWriter(object):

    def __init__(self, output_files):
        self.output_files = output_files

    def handle_data(self, alias, data):
        output_file = os.path.expanduser(self.output_files[alias])
        with open(output_file, 'a') as f:
            if f.tell() == 0:
                f.write('Time,Reading\n')

            send_time = datetime.timedelta(milliseconds=data['send_time'])
            read_time = datetime.timedelta(milliseconds=data["time"])

            device_start_time = datetime.datetime.now() - send_time
            abs_read_time = device_start_time + read_time

            f.write('{},{}, DBUG: {}, {}, {}\n'.format(
                data["value"],
                abs_read_time.strftime("%Y-%m-%d %H:%M:%S"),
                send_time,
                read_time,
                data
            ))
