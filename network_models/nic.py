from resources.resources import interfaces


class NIC:
    def __init__(self, nic_info):
        self.interface = nic_info['name']

        if 'mac' in nic_info and nic_info['mac']:
            self.mac_address = nic_info['mac']
        else:
            self.mac_address = interfaces.create_new_mac()
