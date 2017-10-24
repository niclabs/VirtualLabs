from resources import os_templates, router_templates, switch_templates
from main import connection

templates = {
    'terminal': os_templates,
    'router': router_templates,
    'switch': switch_templates
}


class Template:
    def __init__(self, template_type, info):
        self.name = templates[template_type].get_template(int(info))
        self.template = connection.lookupByName(self.name)

    def get_template_info(self):
        return {'max_memory': self.template.maxMemory(), 'cpus': self.template.maxVcpus()}


