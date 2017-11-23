from virtualLabs.config.default_values import default_link_type
from virtualLabs.checkers.link_info_checker import LinkInfoChecker


class LinkChecker:
    """ Checks the consistency of the information used to create a link between two guests (that the guests and nics
    exists mostly).
    Attributes:
        guest_checker(GuestChecker): Instance of the GuestChecker for this laboratory
        guest_list(list: int, Guest): Dictionary with guests and their ids
    """
    def __init__(self, guest_checker, guest_list):
        """
        :param guest_checker: GuestChecker instance for this laboratory
        :param guest_list: Dictionary with guests and their ids
        """
        self.guest_checker = guest_checker
        self.guest_list = guest_list

    def check_link(self, link_dic):
        """ Checks the consistency for all the link information (endpoints and settings)
        :param link_dic: Dictionary with the link information
        """
        if 'type' not in link_dic:
            link_dic['type'] = default_link_type

        if 'endpoints' not in link_dic:
            raise ValueError("Can not define a link without endpoints")

        for e in link_dic['endpoints']:
            if 'guest' not in e:
                raise ValueError("Can not create a link with no guest at endpoint")

            if 'nic' not in e:
                raise ValueError("Can not create a link with no nic")

            nic_info = self.check_link_guest(e['guest'])
            self.check_link_nic(e['nic'], nic_info)

        if 'settings' in link_dic:
            LinkInfoChecker.check_settings(link_dic['settings'])

    def check_link_guest(self, guest):
        """ Checks if the guest assigned to a link exists.
        :param guest: Dictionary with the guest information to check
        :return: The nics of the guest
        """
        if 'id' in guest:
            if int(guest['id']) not in self.guest_list.keys():
                raise ValueError("Trying to create an endpoint with a non existant guest")
            nic_info = self.guest_list[guest['id']].nics
        elif 'name' in guest:
            if guest['name'] not in self.guest_checker:
                raise ValueError("Trying to create an endpoint with a non existant guest")
            nic_info = self.guest_list[self.guest_checker.get_guest(guest['name'])].nics
        else:
            raise ValueError("An endpoints needs an associated guest")

        return nic_info

    def check_link_nic(self, nic, nic_info):
        """ Checks if the nic assigned to the link exists in the relevant guest
        :param nic: Dictionary with the nic information to check
        :param nic_info: List with the nics of the relevant guest
        """
        if 'id' in nic:
            if int(nic['id']) >= len(nic_info):
                raise ValueError("Can not connect using a non existent nic")
        elif 'name' in nic:
            found_nic = ''
            for n in nic_info:
                if n.interface == nic['name']:
                    found_nic = n
            if not found_nic:
                raise ValueError("Can not connect using a non existent nic")