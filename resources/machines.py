from main import connection
import xmltodict as xd
from templates import Templates

machines_types = ['terminal', 'router', 'switch']


class Machines:
    def __init__(self):
        self.machine_list = self.list_existing_machines()

    @staticmethod
    def list_existing_machines():
        all_machines_list = Templates('').list_templates()
        machine_list = list(filter(lambda x: not x.startswith('template_'), all_machines_list))

        return machine_list

    def get_all_machines_macs(self):
        macs = []

        for machine in self.machine_list:
            macs.extend(self.get_macs(machine))

        return macs

    @staticmethod
    def get_macs(machine):
        macs = []

        domain = connection.lookupByName(machine)
        raw_xml = domain.XMLDesc(0)
        mac_dic = xd.parse(raw_xml, force_list={'interface'})

        if 'interface' in mac_dic['domain']['devices']:
            interfaces = mac_dic['domain']['devices']['interface']
            for i in interfaces:
                macs.append(str(i['mac']['@address']))

        return macs



