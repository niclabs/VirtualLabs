import os


class TextFileController:
    """ Wrapper class that hides the communication with the database
        Attributes:
            labs (dict): Dictionary containing (lab_name, lab_xml_path)
            lab_file (str): Path to the database file
            lab_path (str): Path to the directory where labs are saved
    """
    def __init__(self):
        self.labs = {}
        self.get_labs_from_file()
        self.lab_file = 'lab_models/db/labs.txt'
        self.lab_path = 'saved_labs/'

    def get_labs(self):
        """
        :return: Dictionary with laboratory information
        """
        return self.labs

    def get_labs_from_file(self):
        """ Reads the lab file and fills the lab dictionary
        """
        with open(self.lab_file, 'r') as f:
            self.labs = dict([line.split() for line in f])

    def lab_file_name(self, name):
        """
        :param name: Name of a laboratory
        :return: Path where the lab is to be saved
        """
        return self.lab_path + name

    def save_lab(self, name, path):
        """ Include a new laboratory in the database
        :param name: Name of the laboratory to save
        :param path: Path to the file definining the laboratory
        """
        line = name + " " + path
        with open(self.lab_file, 'a') as f:
            f.write(line + os.linesep)

    def get_lab_file(self, lab_name):
        """ Get the path to the file defining a laboratory
        :param lab_name: Name of the laboratory to find
        :return: Path to the lab file
        """
        if lab_name not in self.labs.keys():
            raise ValueError("Non existant laboratory :(")
        return self.lab_path + self.labs[lab_name]

