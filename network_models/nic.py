
from resources.resources import interfaces


class NIC:
    def __init__(self, nic_info):
        if 'mac' not in nic_info:
            nic_info['mac'] = interfaces.create_new_mac()

        self.interface = nic_info['name']
        self.mac_address = nic_info['mac']
