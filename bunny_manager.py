from __future__ import print_function
import gatt
from functools import partial

SERVICE_UUID = '00002220-0000-1000-8000-00805f9b34fb'
RECEIVE_UUID = '00002221-0000-1000-8000-00805f9b34fb'

class MyDevice(gatt.Device):

    def __init__(self, mac_address, manager, on_device_updated, on_data_received):
        super().__init__(mac_address=mac_address, manager=manager)
        self.on_device_updated = on_device_updated
        self.on_data_received = on_data_received

    def connect(self):
        super().connect()

    def connect_succeeded(self):
        self.on_device_updated('Connected')
        super().connect_succeeded()

    def connect_failed(self, error):
        self.on_device_updated('Connection Failed')
        super().connect_failed(error)

    def disconnect_succeeded(self):
        self.on_device_updated('Disconnected')
        super().disconnect_succeeded()

    def services_resolved(self):
        super().services_resolved()
        self.receive_service = next(
            s for s in self.services
            if s.uuid == SERVICE_UUID)

        self.receive_characteristic = next(
            c for c in self.receive_service.characteristics
            if c.uuid == RECEIVE_UUID)

        self.receive_characteristic.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        super().characteristic_value_updated(characteristic, value)
        read_time_value = value[:4]
        reading_value = value[4:6]
        send_time_value = value[6:10]
        sequence_number_value = value[10:]
        read_time = int.from_bytes(read_time_value, byteorder='little', signed=False)
        reading = int.from_bytes(reading_value, byteorder='little', signed=True)
        send_time = int.from_bytes(send_time_value, byteorder='little', signed=False)
        sequence_number = int.from_bytes(sequence_number_value, byteorder='little', signed=False)

        self.on_data_received({
            'read_time': read_time,
            'value': reading,
            "send_time": send_time,
            "sequence_number": sequence_number,
        })


class MyManager(gatt.DeviceManager):

    def __init__(self, device_aliases, adapter_name, on_device_updated=None, on_data_received=None):
        super().__init__(adapter_name=adapter_name)
        self.device_aliases = device_aliases
        self.connected_devices = {}
        if on_device_updated:
            self.on_device_updated = on_device_updated
        else:
            self.on_device_updated = lambda alias, event: print('{} {}'.format(alias, event))

        if on_data_received:
            self.on_data_received = on_data_received
        else:
            self.on_data_received = lambda alias, value: print('{} {}'.format(alias, value["value"]))

    def device_discovered(self, device):

        if device.alias() not in self.device_aliases:
            return

        mac = device.mac_address
        if device.mac_address in self.connected_devices:
            connected_device = self.connected_devices[mac]
            if not connected_device.is_connected():
                self.on_device_updated(connected_device.alias(), 'Connection Lost')
                self.connected_devices.pop(connected_device.mac_address, None)
                self.update_devices()
            return

        alias = device.alias()
        self.on_device_updated(alias, 'Connecting')
        connected_device = MyDevice(
            mac_address=device.mac_address,
            manager=self,
            on_device_updated=partial(self.on_device_updated, alias),
            on_data_received=partial(self.on_data_received, alias))

        connected_device.connect()
        self.connected_devices[connected_device.mac_address] = connected_device

    def stop(self):
        for mac in self.connected_devices:
            connected_device = self.connected_devices[mac]
            if connected_device.is_connected():
                connected_device.disconnect()

        super().stop()
