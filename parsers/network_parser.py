import xmltodict as xd
from utils.container import Container
from copy import deepcopy


class NetworkParser:
    def __init__(self, xml_path):
        with open(xml_path, 'r') as f:
            self.net_dict = xd.parse(f, force_list={'host', 'clone', 'nic', 'link'})
        self.guests_ids = Container()
        self.links_ids = Container()

    def parse_xml(self):
        for h in self.net_dict['network']['guests']['guest']:
            if '@id' in h:
                self.guests_ids.add_element_with_id(h, int(h['@id']))
            else:
                self.guests_ids.add_element(h)

        for c in self.net_dict['network']['guests']['clone']:
            copies = int(c['@copies']) if '@copies' in c else 1

            if '@start_id' in c:
                start_id = c['@start_id']
                for i in range(0, copies):
                    elem_id = int(start_id) + i
                    elem = deepcopy(c)
                    elem['name'] = elem['name'] + str(elem_id)
                    self.guests_ids.add_element_with_id(elem, elem_id)
            else:
                for i in range(0, copies):
                    elem_id = int(self.guests_ids.next_id) + i
                    elem = deepcopy(c)
                    elem['@name'] = elem['@name'] + str(elem_id)
                    self.guests_ids.add_element_with_id(elem, elem_id)

        for l in self.net_dict['network']['links']['link']:
            self.links[l['@id']] = link.Link(l)

    def get_parsed_network(self):
        self.parse_xml()

