from xml_parsers.link_info_parser import LinkInfoParser


class LinkParser:
    def __init__(self):
        pass

    def parse_link(self, link_dic):
        endpoints = []

        for e in link_dic['endpoints']['endpoint']:
            endpoints.append(self.parse_endpoint(e))

        link = {'endpoints': endpoints, 'settings': self.parse_settings(link_dic)}
        return link

    def parse_external_link(self, link_dic):
        endpoints = []
        for e in link_dic['endpoint']:
            endpoints.append(self.parse_endpoint(e))

        link = {'endpoints': endpoints, 'settings': self.parse_settings(link_dic)}
        return link

    def parse_endpoint(self, e):
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
        settings = {}
        if 'settings' in link_dic:
            settings = LinkInfoParser(link_dic['settings']).get_all_parsed()

        return settings




