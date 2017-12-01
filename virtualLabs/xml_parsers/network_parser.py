from copy import deepcopy
import xmltodict as xd
from virtualLabs.utils.container import Container
from virtualLabs.xml_parsers.batch_link_parser import BatchLinkParser
from virtualLabs.xml_parsers.guest_parser import GuestParser
from virtualLabs.xml_parsers.link_parser import LinkParser
from virtualLabs import path


class NetworkParser:
    """ Parses a network XML, generating dictionaries with the information formatted following the rules of the network model
    classes.
    Attributes:
        net_dict(dict): Dictionary created from the network XML
        guest_id(Container): Keeps all Guest instances and their associated ids
        links_id(Container): Keeps all Link instances and their ids
    """
    def __init__(self, xml_path):
        """
        :param xml_path: Path to the file with the XML that is to be parsed
        """
        real_path = path +  xml_path
        with open(real_path, 'r') as f:
            self.net_dict = xd.parse(f, force_list={'guest', 'clone', 'nic', 'batch_link', 'link'})
        self.guests_ids = Container()
        self.links_ids = Container()

    def parse_xml(self):
        """ Parses the XML
        :return: Dictionary with the parsed network
        """
        guest_parser = GuestParser()

        if 'clone' in self.net_dict['network']['guests']:
            for c in self.net_dict['network']['guests']['clone']:
                copies = int(c['@copies']) if '@copies' in c else 1

                if 'name' not in c:
                    raise ValueError("Can not create a set of machines with no name")

                if '@start_id' in c:
                    start_id = c['@start_id']
                    for i in range(0, copies):
                        elem_id = int(start_id) + i
                        elem = deepcopy(c)
                        elem['name'] = elem['name'] + str(elem_id)

                        parsed_guest = guest_parser.parse_guest(elem)
                        self.guests_ids.add_element_with_id(parsed_guest, elem_id)

                else:
                    for i in range(0, copies):
                        elem_id = int(self.guests_ids.next_id) + i
                        elem = deepcopy(c)
                        elem['name'] = elem['name'] + str(elem_id)

                        parsed_guest = guest_parser.parse_guest(elem)
                        self.guests_ids.add_element_with_id(parsed_guest, elem_id)
        if 'guest' in self.net_dict['network']['guests']:
            for g in self.net_dict['network']['guests']['guest']:
                parsed_guest = guest_parser.parse_guest(g)
                if '@id' in g:
                    self.guests_ids.add_element_with_id(parsed_guest, int(g['@id']))
                else:
                    self.guests_ids.add_element(parsed_guest)

        link_parser = LinkParser()
        batch_link_parser = BatchLinkParser(self.guests_ids.get_dict())

        if 'batch_link' in self.net_dict['network']['links']:
            for lc in self.net_dict['network']['links']['batch_link']:
                parsed_links = batch_link_parser.parse_links(lc)
                for l in parsed_links:
                    self.links_ids.add_element(l)

        if 'link' in self.net_dict['network']['links']:
            for l in self.net_dict['network']['links']['link']:
                parsed_link = link_parser.parse_link(l)
                self.links_ids.add_element(parsed_link)

        if 'external_link' in self.net_dict['network']['links']:
            for l in self.net_dict['network']['links']['external_link']:
                parsed_link = link_parser.parse_external_link(l)
                self.links_ids.add_element(parsed_link)

        return {'guests': self.guests_ids.get_dict(), 'links': self.links_ids.get_dict()}

    def get_parsed_network(self):
        """
        :return: The parsed network as a dictionary
        """
        return self.parse_xml()

