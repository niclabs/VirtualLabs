class LinkParser:
    def __init__(self, guest_name_list, guest_list):
        self.guest_names = guest_name_list
        self.guest_list = guest_list

    def parse_link(self, link_dic):
        if 'endpoints' not in link_dic:
            raise ValueError("Can not define a link without endpoints")

        if len(link_dic['endpoints']['endpoint']) is not 2:
            raise ValueError("A link must have exactly two endpoints")

        for e in link_dic['endpoints']['endpoint']:
            if '@id' in e['guest']:
                if e['guest']['@id'] not in self.guest_list.keys():
                    raise ValueError("Trying to create an endpoint with a non existant guest")

            elif '@name' in e['guest']:
                if e['guest']['@name'] not in self.guest_names:
                    raise ValueError("Trying to create an endpoint with a non existant guest")
            else:
                raise ValueError("An endpoints needs an associated guest")


