from virtualLabs.lab.db.text_file_wrapper import TextFileController
from virtualLabs.lab.db.default_db import saved_labs_path, current_labs_path


class LabDBController:
    """ Class that connects the laboratories with the database
    Attributes:
        saved_labs(TextFileController): Controller of the saved labs database
        current_labs(TextFileController): Controller of the current labs database
    """
    def __init__(self):
        self.saved_labs = TextFileController(saved_labs_path)
        self.current_labs = TextFileController(current_labs_path)

    def load_laboratory(self, lab_name):
        """ Get a laboratory information from the database
        :param lab_name: Name of the laboratory to lookup
        :return Name of the file defining the topology of the lab
        """
        return self.saved_labs.get_lab_file(lab_name)

    def save_laboratory(self, lab_name, network):
        """ Saves a laboratory in the database
        :param lab_name: Name of the laboratory to save
        :param network: Network of the laboratory (that must be save in an xml file)
        """
        lab_filename = self.saved_labs.lab_file_name(lab_name)
        network.to_xml(lab_filename)
        self.saved_labs.save_lab(lab_name, lab_filename)

    def list_labs_names(self):
        """
        :return: List of the names of all saved laboratories
        """
        return self.saved_labs.get_labs().keys()

    def list_current_labs(self):
        """
        :return: list of the names of all current laboratories
        """
        return self.current_labs.get_labs().keys()

    def save_current_lab(self, lab_name, lab_topology):
        """ Saves a laboratory in the current lab database
        :param lab_name: Name of the laboratory
        :param lab_topology: Topology of the laboratory
        """
        lab_filename = self.current_labs.lab_file_name(lab_name)
        lab_topology.to_xml(lab_filename)
        self.current_labs.save_lab(lab_name, lab_filename)






