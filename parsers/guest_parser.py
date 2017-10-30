from network_models.host import Host
from resources.template import templates
from resources.machines import machines_types
from parsers.nic_parser import NICParser


class GuestParser:
    def __init__(self):
        self.original_names = Host.list_existing_machines()
        self.new_names = []
        self.nic_parser = NICParser()

    def parse_guest(self, guest_dic):
        guest = {}

        if guest_dic['name'] in self.original_names:
            raise ValueError("Trying to create guest with already existing name")

        if guest_dic['name'] in self.new_names:
            raise ValueError("Collision of names in the network. Names must be unique.")

        if str(guest_dic['name']).startswith('template_'):
            raise ValueError("Can not name a machine as template")

        if guest_dic['@type'] not in machines_types:
            raise ValueError("Trying to create a non existing machine type")

        if '@name' in guest_dic['template']:
            if guest_dic['template']['@name'] not in templates[guest_dic['@type']]:
                raise ValueError("Trying to create guest with non existing template")
        elif '@id' in guest_dic['template']:
            if int(guest_dic['template']['@id']) >= templates[guest_dic['@type']].number():
                raise ValueError("Trying to create guest with non existing template")
        else:
            raise ValueError("Each machine must be created from a template")

        guest = {'name': str(guest_dic['name']), 'template': str(guest_dic['template']), 'type': guest_dic['@type']}

        self.nic_parser.init_guest()
        nics = []
        if 'nic' in guest_dic['nics']:
            for n in guest_dic['nics']['nic']:
                nics.append(self.nic_parser.parse_nic(n))

        number = int(guest_dic['nics']['number']) if 'number' in guest_dic['nics'] else 0
        for i in range(0, number):
            nics.append(self.nic_parser.parse_nic())

        self.new_names.append(guest_dic['name'])
        return guest, nics

    def get_guests_names(self):
        return self.new_names
