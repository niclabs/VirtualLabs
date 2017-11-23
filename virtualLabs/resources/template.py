from resources import os_templates, router_templates, switch_templates
from virtualLabs import connection


""" List the different templates available by type """
templates = {
    'terminal': os_templates,
    'router': router_templates,
    'switch': switch_templates
}


class Template:
    """ Represents a base virtual machine (a "template"), which  is cloned  to create
    new ones.
    Attributes:
        template_type: Type of machine (router, switch,..)
        name: Name of the template (so it can be found on the host)
    """
    def __init__(self, template_type, info):
        """
        :param template_type: Type of machine
        :param info: Information to search for the template in the host
        """
        self.type = template_type

        if 'id' in info:
            self.name = templates[template_type].get_template(info['id'])
        elif 'name' in info:
            self.name = info['name']
        else:
            raise ValueError("Can not create template with no name or id")
        self.template = connection.lookupByName(self.name)

    def get_template_info(self):
        """
        :return: Information of the resources assigned to the template
        """
        return {'max_memory': self.template.maxMemory(), 'cpus': self.template.maxVcpus()}

    def get_id(self):
        """
        :return: id assigned to the template
        """
        return templates[self.type].get_id(self.name)

    def is_null(self):
        """ Does this class represent a specific machine?
        :return: Always false (as this is a template class)
        """
        return False


class NullTemplate:
    """ Represents a specific virtual machine (not a template that can be cloned)
    """
    def __init__(self):
        pass

    def is_null(self):
        """ Does this class represent a specific machine?
        :return: Always true
        """
        return True
