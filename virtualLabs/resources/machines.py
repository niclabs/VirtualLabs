from virtualLabs import connection
import xmltodict as xd
from templates import Templates


class Machines:
    """ Model the set of all concrete virtual machines defined in the host
    Attributes:
        machine_list(list): list of names of the machines
    """
    def __init__(self):
        self.machine_list = self.list_existing_machines()

    @staticmethod
    def list_existing_machines():
        """ Lists all defined machines on the host (without considering the templates)
        :return: List of names of the machines
        """
        all_machines_list = Templates('').list_templates()
        machine_list = list(filter(lambda x: not x.startswith('template_'), all_machines_list))

        return machine_list

    def get_all_machines_macs(self):
        """ Get all MACs used by the machines on the host
        :return: List of the MACs of all defined machines
        """
        macs = []

        for machine in self.machine_list:
            macs.extend(self.get_macs(machine))

        return macs

    @staticmethod
    def get_macs(machine):
        """ Get the MACs of all interfaces of a given machine
        :param machine: Name of the machine
        :return: List of the mac address
        """
        macs = []

        domain = connection.lookupByName(machine)
        raw_xml = domain.XMLDesc(0)
        mac_dic = xd.parse(raw_xml, force_list={'interface'})

        if 'interface' in mac_dic['domain']['devices']:
            interfaces = mac_dic['domain']['devices']['interface']
            for i in interfaces:
                macs.append(str(i['mac']['@address']))

        return macs



