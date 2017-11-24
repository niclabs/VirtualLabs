import netifaces
import random


class NonCollisionMacGenerator:
    """ Generator of MAC address, that makes sure no collision happens
    Attributes:
        interfaces(list): List of interfaces of the host machine
        mac_addresses(list): List of all occupied MAC addresses
    """
    def __init__(self, other_macs):
        """
        :param other_macs: List of all MAC occupied, but not by the host
        """
        self.interfaces = self.list_interfaces()
        self.mac_adresses = self.list_macs()
        self.mac_adresses.extend(other_macs)

    @staticmethod
    def list_interfaces():
        """
        :return: Interfaces of the host machine
        """
        return netifaces.interfaces()

    def list_macs(self):
        """
        :return: MAC addresses of the interfaces of the host machine
        """
        macs = []
        for interface in self.interfaces:
            interface_info = netifaces.ifaddresses(interface)[netifaces.AF_LINK]
            if interface_info:
                macs.append(interface_info[0]['addr'])

        return macs

    @staticmethod
    def create_mac():
        """ Creates a random unicast MAC address"""
        return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    def create_new_mac(self):
        """ Creates a new MAC address making sure it does not collision with any occupied
        address """
        candidate = self.create_mac()
        while candidate in self.mac_adresses:
            candidate = self.create_mac()

        self.mac_adresses.append(candidate)
        return candidate

    def add_mac_to_list(self, mac):
        """ Adds a MAC to the list of occupied addresses
        :param mac: MAC to add
        """
        self.mac_adresses.append(mac)

    def __contains__(self, item):
        """ Checks if a given address is already occupied
        :param item: MAC to check
        :return: Boolean indicating whether the MAC exists or not
        """
        return item in self.mac_adresses
