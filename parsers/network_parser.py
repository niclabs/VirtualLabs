import xmltodict as xd
from utils.container import Container
from copy import deepcopy
from parsers.link_parser import LinkParser
from parsers.guest_parser import GuestParser


class NetworkParser:
    def __init__(self, xml_path):
        with open(xml_path, 'r') as f:
            self.net_dict = xd.parse(f, force_list={'guest', 'clone', 'nic', 'batch_link', 'link'})
        self.guests_ids = Container()
        self.links_ids = Container()

    def parse_xml(self):
        guest_parser = GuestParser()

        for c in self.net_dict['network']['guests']['clone']:
            copies = int(c['@copies']) if '@copies' in c else 1

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

        for g in self.net_dict['network']['guests']['guest']:
            parsed_guest = guest_parser.parse_guest(g)
            if '@id' in g:
                self.guests_ids.add_element_with_id(parsed_guest, int(g['@id']))
            else:
                self.guests_ids.add_element(parsed_guest)

        link_parser = LinkParser(guest_parser.get_guests_names(), self.guests_ids.get_dict())

        for lc in self.net_dict['network']['links']['batch_link']:
            pass

        for l in self.net_dict['network']['links']['link']:
            parsed_link = link_parser.parse_link(l)
            if '@id' in l:
                self.links_ids.add_element_with_id(parsed_link, int(l['@id']))
            else:
                self.links_ids.add_element(parsed_link)

    def get_parsed_network(self):
        self.parse_xml()

