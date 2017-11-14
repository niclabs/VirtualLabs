from resources.templates import Templates


class Host:
    def __init__(self):
        pass

    @staticmethod
    def list_existing_machines():
        all_machines_list = Templates('').list_templates()
        machine_list = list(filter(lambda x: not x.startswith('template_'), all_machines_list))

        return machine_list



