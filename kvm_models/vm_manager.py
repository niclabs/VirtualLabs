import libvirt
from main import connection
from vm_defaults import *
import xmltodict as xd
from copy import deepcopy
from checkers.vm_checker import VirtualMachineChecker
from kvm_models.memory_manager import MemoryManager


class VirtualMachineManager:
    def __init__(self):
        with open(vm_base_xml, 'r') as f:
            self.base_dic = xd.parse(f)
        self.vm_checker = VirtualMachineChecker()
        self.memory_manager = MemoryManager()

    def define_xml(self, settings):
        new_vm_dic = deepcopy(self.base_dic)
        new_vm_dic['domain']['name'] = settings['name']

        if 'ram' in settings:
            new_vm_dic['domain']['memory'] = settings['ram']
        else:
            new_vm_dic['domain']['memory'] = default_ram

        if 'cores' in settings:
            new_vm_dic['domain']['vcpu'] = settings['cores']
        else:
            new_vm_dic['domain']['vcpu'] = default_cores

        memory_settings = {'name': settings['name'] + '.'}

        new_vm_dic['domain']['devices']['disk'][1]['source']['@file'] = settings['iso_path']

        return xd.unparse(new_vm_dic)

    def create_new_vm(self, vm_settings):
        self.vm_checker.check_vm(vm_settings)
        xml = self.define_xml(vm_settings)
        machine = connection.defineXML(xml)
        return machine

    @staticmethod
    def destroy_vm(machine_name):
        try:
            machine = connection.lookupByName(machine_name)
            machine.undefine()
        except libvirt.libvirtError:
            raise ValueError("The machine to be deleted does not exist")


