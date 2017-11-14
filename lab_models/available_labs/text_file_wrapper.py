import os

lab_file = 'lab_models/available_labs/labs.txt'
labs_path = 'saved_labs/'

class TextFileController:
    def __init__(self):
        self.dict = {}
        self.get_labs_from_file()

    def get_labs(self):
        return self.dict

    def get_labs_from_file(self):
        with open(lab_file, 'r') as f:
            self.dict = dict([line.split() for line in f])

    def format_lab(self, name):
        return name +  labs_path + name

    def save_lab(self, lab_name, lab_file_path):
        with open(lab_file, 'a') as f:
            f.write()

