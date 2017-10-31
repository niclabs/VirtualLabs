class LinkParser:
    def __init__(self, guest_name_list, guest_list):
        self.guest_names = guest_name_list
        self.guest_list = guest_list

    def parse_link(self, link_dic):
        endpoints = []

        if 'endpoints' not in link_dic:
            raise ValueError("Can not define a link without endpoints")

        if len(link_dic['endpoints']['endpoint']) is not 2:
            raise ValueError("A link must have exactly two endpoints")

        for e in link_dic['endpoints']['endpoint']:
            endpoint = ''
            nic_info = []

            if 'link_guest' not in e:
                raise ValueError("Can not create a link with no guest at endpoint")

            if 'link_nic' not in e:
                raise ValueError("Can not create a link with no nic")

            if '@id' in e['link_guest']:
                if int(e['link_guest']['@id']) not in self.guest_list.keys():
                    raise ValueError("Trying to create an endpoint with a non existant guest")
                endpoint = {'id': int(e['link_guest']['@id'])}
                nic_info = self.guest_list[endpoint['id']]['nics']
            elif '@name' in e['link_guest']:
                if e['link_guest']['@name'] not in self.guest_names:
                    raise ValueError("Trying to create an endpoint with a non existant guest")
                endpoint = {'name': str(e['link_guest']['@name'])}
                #nic_info = self.
            else:
                raise ValueError("An endpoints needs an associated guest")

            if '@id' in e['link_nic']:
                if int(e['link_nic']['@id']) >= len(nic_info):
                    raise ValueError("Can not connect using a non existent nic")

