class NICParser:
    """Parses the XML tags related to the NICs definition"""
    def __init__(self):
        pass

    def parse_nics(self, nics_dic):
        """ Parses a given dictionary obtained from an XML, representing a set of NICs
        :param nics_dic: Dictionary with XML format
        :return: Dictionary with the NIC informattion
        """
        nics = []
        for n in nics_dic:
            nics.append(self.parse_nic(n))

        return nics

    @staticmethod
    def parse_nic(nic_dic={}):
        """ Parses a single NIC tag
        :param nic_dic: Dictionary with the XML NIC tag
        :return: Dictionary with the NIC information
        """
        dic = {}
        if 'name' in nic_dic:
            dic['name'] = str(nic_dic['name'])

        if 'mac' in nic_dic:
            mac = nic_dic['mac']
            dic['mac'] = str(mac)

        return dic





