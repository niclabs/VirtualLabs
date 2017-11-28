from virtualLabs.xml_parsers.nic_parser import NICParser
from virtualLabs.xml_parsers.template_parser import TemplateParser


class GuestParser:
    """ Parses the Guest tag from an XML guest tag
    Attributes:
        nic_parser(NICParser): NICParser that will be used to parse the NICs assigned to the guest
        template_parser(TemplateParser): TemplateParser that will be used to extract template information
    """
    def __init__(self):
        self.nic_parser = NICParser()
        self.template_parser = TemplateParser()

    def parse_guest(self, guest_dic):
        """ Parses the tag, given as a dictionary
        :param guest_dic: Dictionary with the guest information from the XML
        :return: Dictionary with the parsed guest information
        """
        guest = {}

        if 'name' in guest_dic:
            guest['name'] = str(guest_dic['name'])

        if '@type' in guest_dic:
            guest['type'] = str(guest_dic['@type'])

        if 'template' in guest_dic:
            guest['template'] = self.template_parser.parse_template(guest_dic['template'])

        nics = []
        if 'nics' in guest_dic:
            if 'number' in guest_dic['nics']:
                number = int(guest_dic['nics']['number'])
                nics.extend([{} for i in range(0, number)])
            if 'nic' in guest_dic['nics']:
                nics.extend(self.nic_parser.parse_nics(guest_dic['nics']['nic']))

        guest['nics'] = nics
        return guest

