import xmltodict as xd
import link
import terminal
import router
import switch

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

    def load_from_xml(self,xml_path):
        with open(xml_path, 'r') as f:
            net_dict = xd.parse(f, force_list={'host','nic','link'})

        self.name = net_dict['network']['name']
        for h in net_dict['network']['hosts']['host']:
            self.hosts[h['@id']] = host_types[h['@type']](h)

        for l in net_dict['network']['links']['link']:
            self.links[l['@id']] = link.Link(l)

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







