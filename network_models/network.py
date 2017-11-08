import terminal
import router
import switch
import link
from xml_parsers.network_parser import NetworkParser
from checkers.guest_checker import GuestChecker
from checkers.nic_checker import NICChecker
from checkers.link_checker import LinkChecker


guests_types = {
    'terminal': lambda x: terminal.Terminal(x),
    'router': lambda x: router.Router(x),
    'switch': lambda x: switch.Switch(x)
}


class Network:
    def __init__(self, name=""):
        self.name = name
        self.guests = {}
        self.links = {}
        self.guest_checker = GuestChecker()
        self.nic_checker = NICChecker()
        self.link_checker = LinkChecker()

    def to_xml(self):
        xml = {}

    def load_from_xml(self, xml_path):
        parser = NetworkParser(xml_path)

        net_dic = parser.get_parsed_network()

        for g_id in net_dic['guests'].keys():
            guest = net_dic['guests'][g_id]
            self.create_guest(guest, g_id)

        for l_id in net_dic['links'].keys():
            l = net_dic['links'][l_id]
            self.create_link(l, l_id)

    def list_hosts(self):
        return self.guests

    def list_links(self):
        return self.links

    def get_guest(self, guest_id):
        return self.guests[guest_id]

    def turn_network_on(self):
        for k, v in self.guests.items():
            v.power_on()

    def construct_topology(self):
        for key, value in self.guests.items():
            value.create_guest()

        for key, value in self.links.items():
            value.connect_guests()

    def clean_up_topology(self):
        for k, v in self.links.items():
            v.clean_up()
        for k, v in self.guests.items():
            v.delete_guest()

    def connect_guests(self, endpoints, link_settings={}):
        link_id = max(self.links.keys()) + 1

        l = {'settings': link_settings, 'endpoints': endpoints}
        new_link = self.create_link(l, link_id)
        new_link.connect_guests()

    def disconnect_guests(self, link_id):
        self.links[link_id].destroy_link()
        self.links.pop(link_id)

    def add_guest(self, guest_dic, guest_id=-1):
        if guest_id < 0:
            guest_id = max(self.guests.keys()) + 1

        return self.create_guest(guest_dic, guest_id)

    def create_guest(self, guest, g_id):
        self.guest_checker.check_guest(guest, g_id, self.nic_checker)
        self.guests[g_id] = guests_types[guest['type']](guest)

        return self.guests[g_id]

    def create_link(self, link_info, link_id):
        self.link_checker.check_link(link_info)
        self.links[link_id] = link.Link(link_id, link_info, self.guests)

        return self.links[link_id]






