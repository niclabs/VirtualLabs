from virtualLabs.xml_parsers.link_setting_parser import LinkSettingsParser


class LinkParser:
    """ Parses the XML tag related to link definition"""
    def __init__(self):
        pass

    def parse_link(self, link_dic):
        """ Parses a simple (internal) link tag
        :param link_dic: Dictionary with the XML link tag
        :return: Dictionary with the link information
        """
        endpoints = []

        for e in link_dic['endpoints']['endpoint']:
            endpoints.append(self.parse_endpoint(e))

        link = {'type': 'internal', 'endpoints': endpoints, 'settings': self.parse_settings(link_dic)}
        return link

    def parse_external_link(self, link_dic):
        """ Parses a external_link tag
        :param link_dic:  Dictionary with the XML external_link tag
        :return: Dictionary with the external link information
        """
        endpoints = []
        for e in link_dic['endpoint']:
            endpoints.append(self.parse_endpoint(e))

        link = {'type': 'external', 'endpoints': endpoints, 'settings': self.parse_settings(link_dic)}
        return link

    def parse_endpoint(self, e):
        """ Parses one of the endpoints of a link (including guest and nic)
        :param e: Dictionary with the endpoint information to parse
        :return: Dictionary with the enpoint formatted as required
        """
        nic = {}
        guest = {}

        if '@id' in e['link_guest']:
            guest['id'] = int(e['link_guest']['@id'])

        if '@name' in e['link_guest']:
            guest['name'] = str(e['link_guest']['@name'])

        if '@id' in e['link_nic']:
            nic['id'] = int(e['link_nic']['@id'])

        if '@name' in e['link_nic']:
            nic['name'] = str(e['link_nic']['@name'])

        return {'guest': guest, 'nic': nic}

    def parse_settings(self, link_dic):
        """ Parses the tags related to the settings of the link
        :param link_dic: Dictionary with the link information
        :return: Dictionary with the settings information parsed
        """
        settings = {}
        if 'settings' in link_dic:
            settings = LinkSettingsParser(link_dic['settings']).get_all_parsed()

        return settings




