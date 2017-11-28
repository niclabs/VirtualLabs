from virtualLabs import connection
from virtualLabs.kvm_models.vm_manager import VirtualMachineManager


class Templates:
    """ Represent a set of templates with a common name prefix
    Attribute:
        regex(str): Common name prefix of all templates
        templates(list): List of templates with the common prefix
        vm_manager(VirtualMachineManager): instance of the class in charge of adding or
        deleting virtual machines (and, hence, also templates)
    """
    def __init__(self, regex):
        """
        :param regex: Prefix used to group the templates
        """
        self.regex = regex
        self.templates = self.get_template_list()
        self.vm_manager = VirtualMachineManager()

    def get_template_list(self):
        """
        :return: List with all machines that have the same prefix
        """
        machines = connection.list_machines()
        return [i for i in machines if i.startswith(self.regex)]

    def get_template(self, template_id):
        """
        :param template_id: Id (position) of a template
        :return: Name of the template of given id
        """
        return self.templates[template_id]

    def list_templates(self):
        """
        :return: List of all templates with the same prefix
        """
        return self.templates

    def __contains__(self, item):
        """ Check if a given item is in this set of templates
        :param item: Item to check
        :return: Boolean indicating the result of the check
        """
        return item in self.templates

    def number(self):
        """
        :return: Number of templates in this set
        """
        return len(self.templates)

    def add_template(self, settings):
        """ Adds a new template to the set (and defines it on the host)
        NOTE: The terminal gets stuck here until the installation of the new machine
        is done.
        :param settings: Properties of the new template
        """
        if 'name' in settings and not settings['name'].startswith(self.regex):
            raise ValueError("Given template name does not coincide with template type")

        self.vm_manager.create_new_vm(settings)
        self.recompute_available()

    def delete_template(self, template_name):
        """ Deletes a template from the set and the host machine
        :param template_name: Name of the template to delete
        """
        self.vm_manager.destroy_vm(template_name)
        self.recompute_available()

    def recompute_available(self):
        """ Updates the set of templates """
        self.templates = self.get_template_list()

    def get_id(self, name):
        """
        :param name: Name of a template
        :return: Id of the given template
        """
        return self.templates.index(name)


class OSTemplates(Templates):
    """ Represents the set of templates that are used create a terminal (PCs)"""
    def __init__(self):
        Templates.__init__(self, 'template_os_')


class RouterTemplates(Templates):
    """ Represents the set of templates that are used to create a router """
    def __init__(self):
        Templates.__init__(self, 'template_router_')


class SwitchTemplates(Templates):
    """ Represents the set of templates that are used to create a switch """
    def __init__(self):
        Templates.__init__(self, 'template_switch_')













