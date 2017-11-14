from checkers.link_info_checker import LinkInfoChecker


class LinkChecker:
    def __init__(self, guest_checker, guest_list):
        self.guest_checker = guest_checker
        self.guest_list = guest_list

    def check_link(self, link_dic):
        if 'endpoints' not in link_dic:
            raise ValueError("Can not define a link without endpoints")

        if len(link_dic['endpoints']) is not 2:
            raise ValueError("A link must have exactly two endpoints")

        for e in link_dic['endpoints']:
            if 'guest' not in e:
                raise ValueError("Can not create a link with no guest at endpoint")

            if 'nic' not in e:
                raise ValueError("Can not create a link with no nic")

            nic_info = self.check_link_guest(e['guest'])
            self.check_link_nic(e['nic'], nic_info)

        if 'settings' in link_dic:
            LinkInfoChecker.check_settings(link_dic['settings'])

    def check_link_guest(self, guest):
        if 'id' in guest:
            if int(guest['id']) not in self.guest_list.keys():
                raise ValueError("Trying to create an endpoint with a non existant guest")
            nic_info = self.guest_list[guest['id']].nics
        elif 'name' in guest:
            if guest['name'] not in self.guest_checker:
                raise ValueError("Trying to create an endpoint with a non existant guest")
            nic_info = self.guest_list[self.guest_checker.get_guest(guest['name'])].nics
        else:
            raise ValueError("An endpoints needs an associated guest")

        return nic_info

    def check_link_nic(self, nic, nic_info):
        if 'id' in nic:
            if int(nic['id']) >= len(nic_info):
                raise ValueError("Can not connect using a non existent nic")
        elif 'name' in nic:
            found_nic = ''
            for n in nic_info:
                if n.interface == nic['name']:
                    found_nic = n
            if not found_nic:
                raise ValueError("Can not connect using a non existent nic")