from main import connection


class OSTemplates:
    def __init__(self):
        machines = connection.list_machines()
        self.templates = [i for i in machines if i.startswith('template_os_')]

    def get_template(self, id):
        return self.templates[id]





class Template:
    def __init__(self, info):
        self.name = templates.get_template(int(info))




