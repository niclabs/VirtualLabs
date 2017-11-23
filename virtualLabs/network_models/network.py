import virtualLabs.network_models.model_types.link_types as ltypes
import xmltodict as xd
from virtualLabs.checkers.guest_checker import GuestChecker
from virtualLabs.checkers.link_checker import LinkChecker

import virtualLabs.linux.linux_utils
import virtualLabs.network_models.model_types.guest_types as gtypes
from virtualLabs.checkers.nic_checker import NICChecker
from virtualLabs.xml_parsers.network_parser import NetworkParser


class Network:
    def __init__(self):
        self.name = ""
        self.guests = {}
        self.links = {}
        self.guest_checker = GuestChecker()
        self.nic_checker = NICChecker()
        self.link_checker = LinkChecker(self.guest_checker, self.guests)

    def name_network(self, name):
        self.name = name
        self.guest_checker.name_lab(self.name)

    def to_xml(self, filename):
        xml = {'network': {
            'guests': [],
            'links': []
            }
        }

        for g_id, g in self.guests.items():
            g_dict = g.to_dict()
            g_dict['@id'] = g_id

            xml['network']['guests'].append(g_dict)

        for l in self.links:
            xml['network']['links'].append(l.to_dict())

        xml_file = virtualLabs.linux.linux_utils.touch(filename)
        xd.unparse(xml, xml_file, pretty=True)
        xml_file.close()

    def create_from_xml(self, xml_path):
        parser = NetworkParser(xml_path)

        net_dic = parser.get_parsed_network()

        for g_id in net_dic['guests'].keys():
            guest = net_dic['guests'][g_id]
            self.add_guest(guest, g_id)

        for l_id in net_dic['links'].keys():
            l = net_dic['links'][l_id]
            self.create_link(l, l_id)

    def list_hosts(self):
        return self.guests

    def list_links(self):
        return self.links

    def get_guest(self, guest_id):
        return self.guests[guest_id]

    def get_guest_by_name(self, guest_name):
        guest_id = self.guest_checker.get_guest(guest_name)
        return self.get_guest(guest_id)

    def turn_network_on(self):
        for k, v in self.guests.items():
            v.power_on()

    def turn_network_off(self):
        for k, v in self.guests.items():
            v.power_off()

    def construct_topology(self):
        for key, value in self.guests.items():
            value.create_guest()

        for key, value in self.links.items():
            value.connect_guests()

    def clean_up_topology(self):
        for k, v in self.links.items():
            v.clean_up()

    def connect_guests(self, link_info):
        self.link_checker.check_link(link_info)
        settings = link_info['settings'] if 'settings' in link_info else {}

        self.connect_guests_parse(link_info, settings)

    def connect_guests_parse(self, endpoints, link_settings):
        link_id = max(self.links.keys()) + 1

        l = {'settings': link_settings, 'endpoints': endpoints}
        new_link = self.create_link(l, link_id)
        new_link.connect_guests()

    def disconnect_guests(self, link_id):
        self.links[link_id].destroy_link()
        self.links.pop(link_id)

    def create_guest(self, guest_dic, guest_id=-1):
        if guest_id < 0:
            guest_id = max(self.guests.keys()) + 1

        return self.add_guest(guest_dic, guest_id)

    def add_guest(self, guest, g_id):
        self.guest_checker.check_guest(guest, g_id, self.nic_checker)
        self.guests[g_id] = gtypes.create_guest_by_type(guest, guest['type'], self.name)

        return self.guests[g_id]

    def create_link(self, link_info, link_id):
        self.links[link_id] = ltypes.create_link_from_type(self.name, link_id, link_info, self.guests,
                                                           self.guest_checker)

        return self.links[link_id]






