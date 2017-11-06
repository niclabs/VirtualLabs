from resources.resources import interfaces


class NICParser:
    def __init__(self):
        self.guest_nic_names = []

    def parse_nic(self, nic_dic={}):
        dic = {}
        if 'name' in nic_dic:
            name = nic_dic['name']
            if name in self.guest_nic_names:
                raise ValueError("Can not repeat nic names")
            self.guest_nic_names.append(name)
            dic['name'] = str(name)

        if 'mac' in nic_dic:
            mac = nic_dic['mac']
            if mac in interfaces:
                raise ValueError("MAC collision!")
            interfaces.add_mac_to_list(mac)
            dic['mac'] = str(mac)

        return dic

    def init_guest(self):
        self.guest_nic_names = []



