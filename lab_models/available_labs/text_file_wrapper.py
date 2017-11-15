import os


class TextFileController:
    def __init__(self):
        self.dict = {}
        self.get_labs_from_file()
        self.lab_file = 'lab_models/available_labs/labs.txt'
        self.lab_path = 'saved_labs/'

    def get_labs(self):
        return self.dict

    def get_labs_from_file(self):
        with open(self.lab_file, 'r') as f:
            self.dict = dict([line.split() for line in f])

    def lab_file_name(self, name):
        return self.lab_path + name

    def save_lab(self, name, path):
        line = name + " " + path
        with open(self.lab_file, 'a') as f:
            f.write(line + os.linesep)



