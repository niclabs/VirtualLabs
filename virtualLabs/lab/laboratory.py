from virtualLabs.lab.lab_db_controller import LabDBController
from virtualLabs.network_models.network import Network


class Laboratory:
    """ Class that represents a virtual laboratory.
    Attributes:
        name (str): Name of the laboratory (identifies it)
        topology (Network): Topology of the network of the laboratory
        db_wrapper (LabDBController): Connection to the lab database
    """
    def __init__(self,name=""):
        self.name = name
        self.topology = Network()
        self.db_wrapper = LabDBController()

    def create_from_xml(self, lab_name, xml_path):
        """ Create an empty laboratory from a topology xml file
        :param lab_name: name of the new laboratory
        :param xml_path: Path to the xml
        """
        self.name = lab_name
        self.topology.name_network(lab_name)
        self.topology.create_from_xml(xml_path)

    def save_laboratory(self):
        """ Save the laboratory in the database"""
        self.db_wrapper.save_laboratory(self.name, self.topology)

    def exit_laboratory(self):
        """ Turn off the virtual machines and clean up resources"""
        self.topology.turn_network_off()
        self.topology.clean_up_topology()

    def load_laboratory(self, lab_name):
        """ Create this laboratory from one saved in the database"""
        self.name = lab_name
        topology_file = self.db_wrapper.load_laboratory(lab_name)
        self.topology.create_from_xml(topology_file)

    def get_topology(self):
        """
        :return: The laboratory topology
        """
        return self.topology

    def name_laboratory(self, lab_name):
        """ Assigns a name to the lab
        :param lab_name: Name if the laboratory
        """
        self.name = lab_name
        self.topology.name_network(self.name)

