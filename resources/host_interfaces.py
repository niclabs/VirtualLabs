import netifaces
import random


class HostInterfaces:
    def __init__(self):
        self.interfaces = self.list_interfaces()
        self.mac_adresses = self.list_macs()

    @staticmethod
    def list_interfaces():
        return netifaces.interfaces()

    def list_macs(self):
        macs = []
        for interface in self.interfaces:
            interface_info = netifaces.ifaddresses(interface)[netifaces.AF_LINK]
            macs.append(interface_info['addr'])

        return macs

    @staticmethod
    def create_mac():
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))

    def create_new_mac(self):
        candidate = self.create_mac()
        while candidate not in self.mac_adresses:
            candidate = self.create_mac()

        return candidate
