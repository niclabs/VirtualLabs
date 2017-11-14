from lab_models.available_labs.text_file_wrapper import TextFileController


class LabDBController:
    def __init__(self):
        self.labs = TextFileController().get_labs()

    def load_laboratory(self, lab_name):
        if lab_name not in self.labs.keys():
            raise ValueError("Non existant laboratory :(")




