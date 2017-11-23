class Endpoint:
    """ Represents a link endpoint, keeping the connected guest and used NIC
    Attributes:
        guest_id: Id of the connected guest
        guest: Guest instance of the connected guest
        nic_id: Id of used NIC
        nic: NIC instance of the used NIC
    """
    def __init__(self, setting, guests, guest_checker):
        """
        :param setting: Information about the endpoint
        :param guests: List of guest
        :param guest_checker: GuestChecker instance to check the guest to connect
        """
        self.guest_id = 0
        self.guest = self.init_guest(setting['guest'], guests, guest_checker)

        self.nic_id = 0
        self.nic = self.init_nic(setting['nic'], self.guest.nics)

    def init_guest(self, guest, guests, guest_checker):
        """ Determines the guest id from the given information
        :param guest: Information of the guest that will be connected
        :param guests: List of guests
        :param guest_checker: GuestChecker (translates name->id)
        :return: Guest instance
        """
        if 'id' in guest:
            self.guest_id = guest['id']

        if 'name' in guest:
            self.guest_id = guest_checker.get_guest(guest['name'])

        return guests[self.guest_id]

    def init_nic(self, nic, nic_info):
        """ Determines the nic id from the given information
        :param nic: Nic information
        :param nic_info: List of nics of the guest to be connected
        :return: NIC instance
        """
        if 'id' in nic:
            self.nic_id = nic['id']
        if 'name' in nic:
            for i in range(0, len(nic_info)):
                if nic_info[i] == nic['name']:
                    self.nic_id = i

        return nic_info[self.nic_id]

    def to_dict(self):
        """
        :return: Dictionary formatted to be written to an XML
        """
        dic = {'link_guest': {'@id': self.guest_id},
               'link_nic': {'@id': self.nic_id}}

        return dic
