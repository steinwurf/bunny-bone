#!/usr/bin/python
import curses
import datetime
import os
import threading
import time
import logging

class CSVResultWriter(object):

    def __init__(self, output_files):
        self.output_files = output_files

    def handle_data(self, alias, data):
        now = datetime.datetime.now()
        output_file = os.path.expanduser(self.output_files[alias])
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'a') as f:
            if f.tell() == 0:
                f.write('Read Time,Send Time,Now,Time,Reading,Sequence Number\n')

            send_time = datetime.timedelta(milliseconds=data['send_time'])
            read_time = datetime.timedelta(milliseconds=data["read_time"])

            device_start_time = now - send_time
            absolut_read_time = device_start_time + read_time

            f.write('{read_time},{send_time},{now},{time},{reading},{sequence_number}\n'.format(
                read_time=data['read_time'],
                send_time=data['send_time'],
                now=int(round(now.timestamp() * 1000)),
                time=absolut_read_time.strftime("%Y-%m-%d %H:%M:%S"),
                reading=data["value"],
                sequence_number=data["sequence_number"]
            ))
            logging.debug('Got data from {} which was powered at {}'.format(alias, device_start_time))

