from network_models.network import Network
from lab_models.lab_loader import LabDBController


class Laboratory:
    def __init__(self, name=''):
        self.name = name
        self.topology = Network()
        self.db_wrapper = LabDBController()

    def create_from_xml(self, xml_path):
        self.topology.create_from_xml(xml_path)

    def save_laboratory(self):
        pass

    def load_laboratory(self, lab_name):
        self.name = lab_name
        self.topology = self.db_wrapper.load_laboratory(lab_name)



