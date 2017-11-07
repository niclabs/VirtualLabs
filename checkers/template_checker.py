from resources.template import templates


class TemplateChecker:
    def __init__(self):
        pass

    def check_template(self, template, guest_type):
        if 'name' in template:
            if template['name'] not in templates[guest_type]:
                raise ValueError("Trying to create guest with non existing template")
        elif 'id' in template:
            if int(template['id']) >= templates[guest_type].number():
                raise ValueError("Trying to create guest with non existing template")
        else:
            raise ValueError("Cannot reference a template without name or id")
