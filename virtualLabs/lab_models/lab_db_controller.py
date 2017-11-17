from virtualLabs.lab_models.db.text_file_wrapper import TextFileController


class LabDBController:
    """ Class that connects the laboratories with the database
    Attributes:
        controller (TextFileController): Controller of the database
    """
    def __init__(self):
        self.controller = TextFileController()

    def load_laboratory(self, lab_name):
        """ Get a laboratory information from the database
        :param lab_name: Name of the laboratory to lookup
        :return Name of the file defining the topology of the lab
        """
        return self.controller.get_lab_file(lab_name)

    def save_laboratory(self, lab_name, network):
        """ Save a laboratory in the database
        :param lab_name: Name of the laboratory to save
        :param network: Network of the laboratory (that must be save in an xml file)
        """
        lab_filename = self.controller.lab_file_name(lab_name)
        network.to_xml(lab_filename)
        self.controller.save_lab(lab_name, lab_filename)

    def list_labs_names(self):
        """
        :return: List of the names of all saved laboratories
        """
        return self.controller.get_labs().keys()




