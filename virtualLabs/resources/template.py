from resources import os_templates, router_templates, switch_templates
from virtualLabs import connection

templates = {
    'terminal': os_templates,
    'router': router_templates,
    'switch': switch_templates
}


class Template:
    def __init__(self, template_type, info):
        self.type = template_type

        if 'id' in info:
            self.name = templates[template_type].get_template(info['id'])
        elif 'name' in info:
            self.name = info['name']
        else:
            raise ValueError("Can not create template with no name or id")
        self.template = connection.lookupByName(self.name)

    def get_template_info(self):
        return {'max_memory': self.template.maxMemory(), 'cpus': self.template.maxVcpus()}

    def get_id(self):
        return templates[self.type].get_id(self.name)

    def is_null(self):
        return False


class NullTemplate:
    def __init__(self):
        pass

    def is_null(self):
        return True
