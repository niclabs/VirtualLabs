from resources.noncollisionmacs import NonCollisionMacGenerator
from resources.machines import Machines
from config.default_names import default_nic


class NICParser:
    def __init__(self):
        self.mac_generator = NonCollisionMacGenerator(Machines.get_all_machines_macs())
        self.guest_nic_names = []
        self.next_nic = 0

    def parse_nic(self, nic_dic):
        name = ''
        mac = ''

        if 'name' in nic_dic:
            name = nic_dic['name']
            if name in self.guest_nic_names:
                raise ValueError("Can not repeat nic names")
        else:
            name = default_nic + str(self.next_nic)

        if 'mac' in nic_dic:
            mac = nic_dic['mac']
            if mac in self.mac_generator:
                raise ValueError("MAC collision!")
            self.mac_generator.add_mac_to_list(mac)
        else:
            mac = self.mac_generator.create_new_mac()

        self.guest_nic_names.append(name)
        return {'name': name, 'mac': mac}

    def init_guest(self):
        self.guest_nic_names = []
        self.next_nic = 0



