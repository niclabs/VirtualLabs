from lab_models.available_labs.text_file_wrapper import TextFileController


class LabDBController:
    def __init__(self):
        self.controller = TextFileController()
        self.labs = self.controller.get_labs()

    def load_laboratory(self, lab_name):
        if lab_name not in self.labs.keys():
            raise ValueError("Non existant laboratory :(")






    def save_laboratory(self, lab_name, network):
        lab_filename = self.controller.lab_file_name(lab_name)
        network.to_xml(lab_filename)
        self.controller.save_lab(lab_name, lab_filename)




