class Endpoint:
    def __init__(self, setting, guests):
        self.guest = guests[setting['id']]
        self.nic = setting['nic']
