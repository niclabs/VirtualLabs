from network_models.host import Host
from resources.machines import machines_types
from config.default_values import *
from checkers.template_checker import TemplateChecker


class GuestChecker:
    def __init__(self, lab_name):
        self.lab_name = lab_name
        self.original_names = Host.list_existing_machines()
        self.new_names = {}
        self.template_checker = TemplateChecker()

    def check_guest(self, guest, guest_id, nic_checker):
        if 'type' not in guest:
            guest['type'] = default_type

        if guest['type'] not in machines_types:
            raise ValueError("Trying to create a non existing machine type")

        if 'template' in guest:
            self.template_checker.check_template(guest['template'], guest['type'])

        if 'template' not in guest and 'name' not in guest:
            raise ValueError("Can not use a base machine with no name")

        if 'template' not in guest:
            base_name = self.lab_name + "_" + guest['name']

            if base_name not in self.original_names:
                raise ValueError("Can not use a non existent machine as base")

        if 'name' not in guest:
            guest['name'] = default_machine[guest['type']] + str(guest_id)

        if guest['name'] in self.original_names:
            raise ValueError("Trying to create guest with already existing name")

        if guest['name'] in self.new_names.keys():
            raise ValueError("Collision of names in the network. Names must be unique.")

        if str(guest['name']).startswith('template_'):
            raise ValueError("Can not name a machine as template")

        if 'nics' in guest:
            nic_checker.init_guest()
            nic_checker.check_nics(guest['nics'])

    def get_guests_names(self):
        return self.new_names

    def add_id_to_guest(self, guest_name, guest_id):
        self.new_names[guest_name] = guest_id

    def __contains__(self, item):
        return item in self.new_names.keys()

    def get_guest(self, name):
        return self.new_names[name]



