from network_models.host import Host
from resources.template import templates
from resources.machines import machines_types
from parsers.nic_parser import NICParser


class GuestParser:
    def __init__(self):
        self.guest_names = Host.list_existing_machines()
        self.nic_parser = NICParser()

    def parse_guest(self, guest_dic):
        guest = {}

        if guest_dic['name'] in self.guest_names:
            raise ValueError("Trying to create guest with already existing name")

        if str(guest_dic['name']).startswith('template_'):
            raise ValueError("Can not name a machine as template")

        if guest_dic['@type'] not in machines_types:
            raise ValueError("Trying to create a non existing machine type")

        if guest_dic['template'] not in templates[guest_dic['@type']]:
            raise ValueError("Trying to create guest with non existing template")

        guest = {'name': guest_dic['name'], 'template': guest_dic['template'], 'type': guest_dic['@type']}

        self.nic_parser.init_guest()
        nics = []
        for n in guest_dic['nics']['nic']:
            nics.append()

        number = int(guest_dic['nics']['number']) if 'number' in guest_dic['number'] else 0


        return guest, nics