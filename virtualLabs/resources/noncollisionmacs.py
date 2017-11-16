import netifaces
import random


class NonCollisionMacGenerator:
    def __init__(self, other_macs):
        self.interfaces = self.list_interfaces()
        self.mac_adresses = self.list_macs()
        self.mac_adresses.extend(other_macs)

    @staticmethod
    def list_interfaces():
        return netifaces.interfaces()

    def list_macs(self):
        macs = []
        for interface in self.interfaces:
            interface_info = netifaces.ifaddresses(interface)[netifaces.AF_LINK]
            if interface_info:
                macs.append(interface_info[0]['addr'])

        return macs

    @staticmethod
    def create_mac():
        return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    def create_new_mac(self):
        candidate = self.create_mac()
        while candidate in self.mac_adresses:
            candidate = self.create_mac()

        self.mac_adresses.append(candidate)
        return candidate

    def add_mac_to_list(self, mac):
        self.mac_adresses.append(mac)

    def __contains__(self, item):
        return item in self.mac_adresses
