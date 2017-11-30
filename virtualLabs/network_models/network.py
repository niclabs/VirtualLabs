import virtualLabs.network_models.model_types.link_types as ltypes
import xmltodict as xd
from virtualLabs.checkers.guest_checker import GuestChecker
from virtualLabs.checkers.link_checker import LinkChecker

import virtualLabs.linux.linux_utils
import virtualLabs.network_models.model_types.guest_types as gtypes
from virtualLabs.checkers.nic_checker import NICChecker
from virtualLabs.xml_parsers.network_parser import NetworkParser

from virtualLabs.utils.functions import get_max


class Network:
    """ Models a network (the topology of the laboratory).
    Attributes:
        name(str): Name of the network (the same of the laboratory)
        guests(list): List of the Guest instances of the network
        links(list): List of the Link instances of the network
        guest_checker(GuestChecker): GuestChecker used to check the consistency of the guest information
        before creating them
        nic_checker(NICChecker): NICChecker used to check or create interfaces names and mac addresses
        link_checker(LinkChecker): LinkChecker used to check the consistency of the link information
    """
    def __init__(self):
        self.name = ""
        self.guests = {}
        self.links = {}
        self.guest_checker = GuestChecker()
        self.nic_checker = NICChecker()
        self.link_checker = LinkChecker(self.guest_checker, self.guests)

    def name_network(self, name):
        """ Assigns a name to the network
        :param name: Name of the network
        """
        self.name = name
        self.guest_checker.name_lab(self.name)

    def to_xml(self, filename):
        """ Formats the network contents as an XML, and then writes it in a file
        :param filename: File where the XML will be written
        """
        xml = {'network': {
            'guests': [],
            'links': []
            }
        }

        for g_id, g in self.guests.items():
            g_dict = g.to_dict()
            g_dict['@id'] = g_id

            xml['network']['guests'].append(g_dict)

        for l_id, l in self.links.items():
            xml['network']['links'].append(l.to_dict())

        xml_file = virtualLabs.linux.linux_utils.touch(filename)
        xd.unparse(xml, xml_file, pretty=True)
        xml_file.close()

    def create_from_xml(self, xml_path):
        """ Fills a network with the information obtained from an XML file
        :param xml_path: File to the XML
        """
        parser = NetworkParser(xml_path)

        net_dic = parser.get_parsed_network()

        for g_id in net_dic['guests'].keys():
            guest = net_dic['guests'][g_id]
            self.add_guest(guest, g_id)

        for l_id in net_dic['links'].keys():
            l = net_dic['links'][l_id]
            self.add_link(l, l_id)

    def list_guests(self):
        """
        :return: List of guests of the network
        """
        return self.guests

    def list_links(self):
        """
        :return: List of links of the network
        """
        return self.links

    def get_guest(self, guest_id):
        """
        :param guest_id: A guest id
        :return: Guest with the given id
        """
        return self.guests[guest_id]

    def get_guest_by_name(self, guest_name):
        """
        :param guest_name: A guest name
        :return: Guest with the given name
        """
        guest_id = self.guest_checker.get_guest(guest_name)
        return self.get_guest(guest_id)

    def turn_network_on(self):
        """ Turns on all the network guests """
        for k, v in self.guests.items():
            v.power_on()

    def turn_network_off(self):
        """ Turns off all the network guests"""
        for k, v in self.guests.items():
            v.power_off()

    def construct_topology(self):
        """ Creates the topology related to the network. Creates the guests and connects them"""
        for key, value in self.guests.items():
            value.create_guest()

        for key, value in self.links.items():
            value.connect_guests()

    def clean_up_topology(self):
        """ Deletes the bridges associated with the links """
        for k, v in self.links.items():
            v.clean_up()

    def create_link(self, link_info):
        """ Creates a link in the network
        :param link_info: Information to create the link
        """
        self.link_checker.check_link(link_info)
        settings = link_info['settings'] if 'settings' in link_info else {}

        return self.create_link_parse(link_info['endpoints'], settings)

    def create_link_parse(self, endpoints, settings):
        """ Creates a link receiving the endpoints and the settings
        :param endpoints:
        :param settings:
        :return:
        """
        link_id = get_max(self.links.keys()) + 1

        l = {'settings': settings, 'endpoints': endpoints}
        return self.add_link(l, link_id)

    def connect_guests(self, link_info):
        """ Connects guests (either between them or with the internet)
        :param link_info: Information about the link (involved guests and nics)
        """
        new_link = self.create_link(link_info)
        new_link.connects_guests()

    def disconnect_guests(self, link_id):
        """ Deletes a link from the network (disconnects one or two guests depending on link type)
        :param link_id: id of the link to delete
        """
        self.links[link_id].destroy_link()
        self.links.pop(link_id)

    def create_guest(self, guest_dic, guest_id=-1):
        """ Adds a new guest to the network
        :param guest_dic: Dictionary with the guest information
        :param guest_id: Optional id to assign to the guest (created by default if none is given)
        :return: The created Guest instance
        """
        if guest_id < 0:
            guest_id = get_max(self.guests.keys()) + 1

        return self.add_guest(guest_dic, guest_id)

    def add_guest(self, guest, g_id):
        """ Adds a new guest to the network given an id
        :param guest: Guest information
        :param g_id: Guest id
        :return: The new Guest instance
        """
        self.guest_checker.check_guest(guest, g_id, self.nic_checker)
        self.guests[g_id] = gtypes.create_guest_by_type(guest, guest['type'], self.name)
        self.guest_checker.add_id_to_guest(self.guests[g_id].get_name(), g_id)

        return self.guests[g_id]

    def add_link(self, link_info, link_id):
        """ Creates a new link given an id
        :param link_info: Link information
        :param link_id: Link id
        :return: The new Link instance
        """
        self.links[link_id] = ltypes.create_link_from_type(self.name, link_id, link_info, self.guests,
                                                           self.guest_checker)

        return self.links[link_id]






