from network_models.host import Host
from resources.machines import machines_types
from config.default_values import *
from checkers.template_checker import TemplateChecker


class GuestChecker:
    def __init__(self):
        self.original_names = Host.list_existing_machines()
        self.new_names = {}
        self.template_checker = TemplateChecker()

    def check_guest(self, guest, guest_id, nic_checker):
        if 'type' not in guest:
            guest['type'] = default_type

        if guest['type'] not in machines_types:
            raise ValueError("Trying to create a non existing machine type")

        if 'name' not in guest:
            guest['name'] = default_machine[guest['type']] + str(guest_id)

        if guest['name'] in self.original_names:
            raise ValueError("Trying to create guest with already existing name")

        if guest['name'] in self.new_names.keys():
            raise ValueError("Collision of names in the network. Names must be unique.")

        if str(guest['name']).startswith('template_'):
            raise ValueError("Can not name a machine as template")

        if 'template' not in guest:
            raise ValueError("Each machine must be created from a template")

        if 'nics' in guest:
            nic_checker.init_guest()
            nic_checker.check_nics(guest['nics'])

        self.template_checker.check_template(guest['template'])


