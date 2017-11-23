from virtualLabs.config.default_values import *
from virtualLabs.checkers.template_checker import TemplateChecker
from virtualLabs.resources.machines import Machines
from virtualLabs.network_models.model_types.guest_types import guests_types


class GuestChecker:
    """ In charge of checking the consistency of the parameters for all guest creation
    Attributes:
        lab_name(str): Name of the laboratory the guests will belong to
        original_names(list: str): List of the machines previously existent in the host
        new_names(dict: name, int): Dictionary with the names of the laboratory's guest and their ids
    """
    def __init__(self):
        self.lab_name = ""
        self.original_names = Machines.list_existing_machines()
        self.new_names = {}

    def name_lab(self, lab_name):
        """
        :param lab_name: Name of the laboratory the check guests belong to
        """
        self.lab_name = lab_name

    def check_guest(self, guest, guest_id, nic_checker):
        """
        Checks the consistency of the parameters for the creation of a guest
        :param guest: Dictionary with guest information
        :param guest_id: Id to assign to the guest
        :param nic_checker: NICChecker used to validate the guest NIC information
        """

        if 'type' not in guest:
            guest['type'] = default_type

        if guest['type'] not in guests_types.keys():
            raise ValueError("Trying to create a non existing machine type")

        if 'template' in guest:
            TemplateChecker().check_template(guest['template'], guest['type'])

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
        """
        :return: The dictionary with the names and ids of the guests of a laboratory
        """
        return self.new_names

    def add_id_to_guest(self, guest_name, guest_id):
        """
        Adds a new guest name to the guest_names dictionary
        :param guest_name: Name to set as key
        :param guest_id: Id to set as value
        """
        self.new_names[guest_name] = guest_id

    def __contains__(self, item):
        return item in self.new_names.keys()

    def get_guest(self, name):
        """
        :param name: Guest name
        :return: Id related to the guest
        """
        return self.new_names[name]



