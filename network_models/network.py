import terminal
import router
import switch
from parsers.network_parser import NetworkParser
from parsers.guest_parser import GuestParser


host_types = {
    'terminal': lambda x: terminal.Terminal(x),
    'router': lambda x: router.Router(x),
    'switch': lambda x: switch.Switch(x)
}


class Network:
    def __init__(self, name=""):
        self.name = name
        self.hosts = {}
        self.links = {}

    def to_xml(self):
        xml = {}

    def load_from_xml(self, xml_path):
        parser = NetworkParser(xml_path)

        net_dic = parser.get_parsed_network()





    def list_hosts(self):
        return self.hosts

    def get_host(self, host_id):
        return self.hosts[host_id]

    def turn_on(self):
        for k, v in self.hosts.items():
            v.power_on()

    def construct_topology(self):
        for key, value in self.hosts.items():
            value.create_host()

        for key, value in self.links.items():
            value.connect_hosts(self.hosts)

    def clean_up_topology(self):
        for k, v in self.links.items():
            v.clean_up()
        for k, v in self.hosts.items():
            v.delete_host()

    def connect_hosts(self, host1, host2):
        pass







