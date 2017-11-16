class Endpoint:
    def __init__(self, setting, guests, guest_checker):
        self.guest_id = 0
        self.guest = self.init_guest(setting['guest'], guests, guest_checker)

        self.nic_id = 0
        self.nic = self.init_nic(setting['nic'], self.guest.nics)

    def init_guest(self, guest, guests, guest_checker):
        if 'id' in guest:
            self.guest_id = guest['id']

        if 'name' in guest:
            self.guest_id = guest_checker.get_guest(guest['name'])

        return guests[self.guest_id]

    def init_nic(self, nic, nic_info):
        if 'id' in nic:
            self.nic_id = nic['id']
        if 'name' in nic:
            for i in range(0, len(nic_info)):
                if nic_info[i] == nic['name']:
                    self.nic_id = i

        return nic_info[self.nic_id]

    def to_dict(self):
        dic = {'link_guest': {'@id': self.guest_id},
               'link_nic': {'@id': self.nic_id}}

        return dic
