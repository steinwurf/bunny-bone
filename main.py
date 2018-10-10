import threading
import argparse
import configparser
import logging

from bunny_manager import MyManager
from bunny_display import Display
from bunny_result_writer import CSVResultWriter

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='bunny_bone.log',level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Bunny Bone Reciever.')
    parser.add_argument(
        'config',
        type=argparse.FileType('r'),
        help='Path to config file.')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read_file(args.config)

    adapter_name = config['DEFAULT']['AdapterName']
    device_aliases = config.sections()
    output_files = {s : config[s]['OutputFile'] for s in device_aliases }

    display = Display(aliases=device_aliases)
    result_writer = CSVResultWriter(output_files=output_files)
    def handle_data(alias, data):
        display.handle_data(alias, data)
        result_writer.handle_data(alias, data)

    manager = MyManager(
        device_aliases=device_aliases,
        adapter_name=adapter_name,
        on_data_received=handle_data,
        on_device_updated=display.handle_event)
    manager.start_discovery()
    display.start()
    thread = threading.Thread(target=manager.run)
    thread.start()

    while True:
        cmd = display.getch()
        if cmd == ord("q"):
            display.stop()
            break

    manager.stop()
    thread.join(10)

if __name__ == '__main__':
    main()
