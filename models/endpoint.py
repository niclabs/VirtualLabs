class Endpoint:
    def __init__(self, setting, hosts):
        self.host = hosts[setting['host'][0]['@id']]
        self.nic = setting['nic'][0]['@id']
