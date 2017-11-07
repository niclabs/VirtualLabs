from resources.resources import interfaces


class NICChecker:
    def __init__(self):
        self.guest_nic_names = []

    def check_nics(self, nics_dic):
        self.init_guest()
        for n in nics_dic:
            self.check_nic(n)

    def check_nic(self, nic_dic):
        if 'name' in nic_dic:
            if nic_dic['name'] in self.guest_nic_names:
                raise ValueError("Can not repeat nic names")
            self.guest_nic_names.append(nic_dic['name'])

        if 'mac' in nic_dic:
            if nic_dic['mac'] in interfaces:
                raise ValueError("MAC collision!")
            interfaces.add_mac_to_list(str(nic_dic['mac']))

    def init_guest(self):
        self.guest_nic_names = []
