class Endpoint:
    def __init__(self, setting, guests):
        self.guest = guests[setting['id']]

        if 'nic' in setting:
            self.nic = setting['nic']
        elif 'nic_id' in setting:
            self.nic = self.guest.get_nic(setting['nic_id'])
