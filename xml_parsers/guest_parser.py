from xml_parsers.nic_parser import NICParser
from xml_parsers.template_parser import TemplateParser


class GuestParser:
    def __init__(self):
        self.nic_parser = NICParser()
        self.template_parser = TemplateParser()

    def parse_guest(self, guest_dic):
        guest = {}

        if 'name' in guest_dic:
            guest['name'] = str(guest_dic['name'])

        if '@type' in guest_dic:
            guest['type'] = str(guest_dic['@type'])

        if 'template' in guest_dic:
            guest['template'] = self.template_parser.parse_template(guest_dic['template'])

        nics = []
        if 'nics' in guest_dic:
            nics.append(self.nic_parser.parse_nics(guest_dic['nics']))

        if 'number' in guest_dic:
            number = int(guest_dic['nics']['number'])
            nics.append([{} for i in range(0, number)])

        guest['nics'] = nics
        return guest
