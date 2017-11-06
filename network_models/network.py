import terminal
import router
import switch
import link
from parsers.network_parser import NetworkParser


guests_types = {
    'terminal': lambda x: terminal.Terminal(x),
    'router': lambda x: router.Router(x),
    'switch': lambda x: switch.Switch(x)
}


class Network:
    def __init__(self, name=""):
        self.name = name
        self.guests = {}
        self.links = {}

    def to_xml(self):
        xml = {}

    def load_from_xml(self, xml_path):
        parser = NetworkParser(xml_path)

        net_dic = parser.get_parsed_network()

        for g_id in net_dic['guests'].keys():
            guest = net_dic['guests'][g_id]
            self.guests[g_id] = guests_types[guest['type']](guest)

        for l_id in net_dic['links'].keys():
            l = net_dic['links'][l_id]
            self.links[l_id] = link.Link(l_id, l, self.guests)

    def list_hosts(self):
        return self.guests

    def get_guest(self, guest_id):
        return self.guests[guest_id]

    def turn_on(self):
        for k, v in self.guests.items():
            v.power_on()

    def construct_topology(self):
        for key, value in self.guests.items():
            value.create_guest()

        for key, value in self.links.items():
            value.connect_guests()

    def clean_up_topology(self):
        for k, v in self.links.items():
            v.clean_up()
        for k, v in self.guests.items():
            v.delete_guest()

    def connect_guests_online(self, guest1, guest2):
        pass







