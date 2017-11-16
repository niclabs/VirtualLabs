from virtualLabs.lab_models.db.text_file_wrapper import TextFileController


class LabDBController:
    def __init__(self):
        self.controller = TextFileController()

    def load_laboratory(self, lab_name):
        return self.controller.get_lab_file(lab_name)

    def save_laboratory(self, lab_name, network):
        lab_filename = self.controller.lab_file_name(lab_name)
        network.to_xml(lab_filename)
        self.controller.save_lab(lab_name, lab_filename)

    def list_labs_names(self):
        return self.controller.get_labs().keys()




