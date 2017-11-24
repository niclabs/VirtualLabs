from virtualLabs.resources.resources import interfaces


class NIC:
    """ Represents a single NIC (Network Interface Card)
    Attributes:
        interface(str): name of the interface
        mac_address(str): MAC address of the NIC (48 bits)
    """
    def __init__(self, nic_info):
        """
        :param nic_info: Dictionary with the information about this NIC
        """
        if 'mac' not in nic_info:
            nic_info['mac'] = interfaces.create_new_mac()

        self.interface = nic_info['name']
        self.mac_address = nic_info['mac']

    def to_dict(self):
        """ Creates a dictionary to save the NIC to an XML
        :return: Dictionary with the NIC information
        """
        dic = {'nic': {
                'name': self.interface,
                'mac': self.mac_address
            }
        }
        return dic
