from virtualLabs.resources.template import templates


class TemplateChecker:
    """ In charge of checking the information used to create a virtual machine from a template
    """
    def __init__(self):
        pass

    def check_template(self, template, guest_type):
        """
        Check the consistency of the information for a given template
        :param template: Dictionary with the template information
        :param guest_type: Type of guest that will be created
        """
        if 'name' in template:
            if template['name'] not in templates[guest_type]:
                raise ValueError("Trying to create guest with non existing template")
        elif 'id' in template:
            if int(template['id']) >= templates[guest_type].number():
                raise ValueError("Trying to create guest with non existing template")
        else:
            raise ValueError("Cannot reference a template without name or id")
