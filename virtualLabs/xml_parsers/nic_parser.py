class NICParser:
    def __init__(self):
        pass

    def parse_nics(self, nics_dic):
        nics = []
        for n in nics_dic:
            nics.append(self.parse_nic(n))

        return nics

    @staticmethod
    def parse_nic(nic_dic={}):
        dic = {}
        if 'name' in nic_dic:
            dic['name'] = str(nic_dic['name'])

        if 'mac' in nic_dic:
            mac = nic_dic['mac']
            dic['mac'] = str(mac)

        return dic





