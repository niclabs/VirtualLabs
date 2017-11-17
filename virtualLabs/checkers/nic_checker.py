from virtualLabs.resources.resources import interfaces


class NICChecker:
    """ Checks the consistency of the information for the creation of a Network Interface Card (NIC)
    Attributes:
        guest_nic_names(list: str): List with the nic names assigned so far for a single guest
    """
    def __init__(self):
        self.guest_nic_names = []

    def check_nics(self, nics_dic):
        """ Check several nics of the same guest
        :param nics_dic: List with several nics to check
        """
        self.init_guest()
        for n in nics_dic:
            self.check_nic(n)

    def check_nic(self, nic_dic):
        """ Checks the consistency of a single nic
        :param nic_dic: Dictionary with nic information
        """
        if 'name' in nic_dic:
            if nic_dic['name'] in self.guest_nic_names:
                raise ValueError("Can not repeat nic names")
            self.guest_nic_names.append(nic_dic['name'])

        if 'mac' in nic_dic:
            if nic_dic['mac'] in interfaces:
                raise ValueError("MAC collision!")
            interfaces.add_mac_to_list(str(nic_dic['mac']))

    def init_guest(self):
        """ Empties the nic_names list to check a new guest
        """
        self.guest_nic_names = []
