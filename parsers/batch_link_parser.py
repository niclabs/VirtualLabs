from parsers.link_info_parser import LinkInfoParser


class BatchLinkParser:
    def __init__(self, guest_list):
        self.guest_list = guest_list

    def parse_links(self, batch_dic):
        endpoints = [[], []]
        links = []

        if 'endpoints' not in batch_dic:
            raise ValueError("Can not define a link without endpoints")

        if len(batch_dic['endpoints']['endpoint']) is not 2:
            raise ValueError("A link must have exactly two endpoints")

        for i in range(0, 2):
            endpoint = batch_dic['endpoints']['endpoint'][i]

            if 'link_guests' in endpoint and 'link_nics' in endpoint:
                raise ValueError("Can not set multiple guests with multiple nics at the same time")

            if 'link_guests' not in endpoint and 'link_nics' not in endpoint:
                raise ValueError("Can not set a single link as a batch")

            if 'link_guests' in endpoint and 'link_nic' in endpoint and '@id' in endpoint['link_nic']:
                nic_id = int(endpoint['link_nic']['@id'])
                if 'from' in endpoint['link_guests'] and '@id' in endpoint['link_guests']['from'] and \
                        'to' in endpoint['link_guests'] and '@id' in endpoint['link_guests']['to']:
                    from_id = int(endpoint['link_guests']['from']['@id'])
                    to_id = int(endpoint['link_guests']['to']['@id'])

                    if from_id in self.guest_list.keys() and to_id in self.guest_list.keys():
                        for j in range(from_id, to_id+1):
                            guest_nic_info = self.guest_list[j]['nics']

                            if nic_id < len(guest_nic_info):
                                endpoints[i].append({'id': j, 'nic': guest_nic_info[nic_id]})
                            else:
                                raise ValueError("Can not create link with non existent nic")
                    else:
                        raise ValueError("Can not create links with non existent guests")
            elif 'link_nics' in endpoint and 'link_guest' in endpoint and '@id' in endpoint['link_guest']:
                guest_id = int(endpoint['link_guest']['@id'])
                guest_nic_info = self.guest_list[guest_id]['nics']
                if 'from' in endpoint['link_nics'] and '@id' in endpoint['link_nics']['from'] and \
                        'to' in endpoint['link_nics'] and '@id' in endpoint['link_nics']['to']:
                    from_id = int(endpoint['link_nics']['from']['@id'])
                    to_id = int(endpoint['link_nics']['to']['@id'])

                    if from_id < len(guest_nic_info) and to_id < len(guest_nic_info):
                        for nic_id in range(from_id, to_id+1):
                            endpoints[i].append({'id': guest_id, 'nic': guest_nic_info[nic_id]})
                    else:
                        raise ValueError("Can not set non existent nics to links")
            else:
                raise ValueError("Can not set the nic to the guests")

        settings = {}
        if 'settings' in batch_dic:
            settings = LinkInfoParser(batch_dic['settings']).get_all_parsed()

        if len(endpoints[0]) is not len(endpoints[1]):
            raise ValueError("Can not pair endpoints, number inconsistent")
        else:
            for e in range(0, len(endpoints[0])):
                links.append({'endpoints': [endpoints[0][e], endpoints[1][e]], 'settings': settings})

        return links
