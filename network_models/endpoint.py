class Endpoint:
    def __init__(self, setting, hosts):
        self.host = hosts[setting['id']]
        self.nic = setting['nic']
