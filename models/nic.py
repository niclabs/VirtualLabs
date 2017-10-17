class NIC:
    def __init__(self, nic_info):
        self.interface = nic_info['name']
        self.mac_address = nic_info['mac']

