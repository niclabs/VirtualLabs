class Endpoint:
    def __init__(self, setting, guests, guest_checker):
        self.guest = self.init_guest(setting['guest'], guests, guest_checker)
        self.nic = self.init_nic(setting['nic'], self.guest.nics)

    @staticmethod
    def init_guest(guest, guests, guest_checker):
        if 'id' in guest:
            return guests[guest['id']]

        if 'name' in guest:
            return guests[guest_checker.get_guest(guest['name'])]

    @staticmethod
    def init_nic(nic, nic_info):
        if 'id' in nic:
            return nic_info[nic['id']]
        elif 'name' in nic:
            for n in nic_info:
                if n == nic['name']:
                    return n