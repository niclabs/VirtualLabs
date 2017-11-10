from main import connection
from kvm_models.vm_manager import VirtualMachineManager


class Templates:
    def __init__(self, regex):
        self.regex = regex
        self.templates = self.get_template_list()
        self.vm_manager = VirtualMachineManager()

    def get_template_list(self):
        machines = connection.list_machines()
        return [i for i in machines if i.startswith(self.regex)]

    def get_template(self, template_id):
        return self.templates[template_id]

    def list_templates(self):
        return self.templates

    def __contains__(self, item):
        return item in self.templates

    def number(self):
        return len(self.templates)

    def add_template(self, settings):
        if 'name' in settings and not settings['name'].startswith(self.regex):
            raise ValueError("Given template name does not coincide with template type")

        self.vm_manager.create_new_vm(settings)
        self.recompute_available()

    def delete_template(self, template_name):
        self.vm_manager.destroy_vm(template_name)
        self.recompute_available()

    def recompute_available(self):
        self.templates = self.get_template_list()

    def get_id(self, name):
        return self.templates.index(name)


class OSTemplates(Templates):
    def __init__(self):
        Templates.__init__(self, 'template_os_')


class RouterTemplates(Templates):
    def __init__(self):
        Templates.__init__(self, 'template_router_')


class SwitchTemplates(Templates):
    def __init__(self):
        Templates.__init__(self, 'template_switch_')













