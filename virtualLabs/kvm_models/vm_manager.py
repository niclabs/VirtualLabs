import libvirt
import subprocess

from virtualLabs import connection
from virtualLabs.checkers.vm_checker import VirtualMachineChecker
from vm_defaults import *


class VirtualMachineManager:
    def __init__(self):
        self.vm_checker = VirtualMachineChecker()

    def create_new_vm(self, vm_settings):
        self.vm_checker.check_vm(vm_settings)

        if 'ram' in vm_settings:
            ram = vm_settings['ram']
        else:
            ram = default_ram

        if 'cores' in vm_settings:
            cores = vm_settings['cores']
        else:
            cores = default_cores

        if 'memory' in vm_settings:
            memory_size = vm_settings['size']
        else:
            memory_size = default_memory_size

        subprocess.call(['virt-install', '--name', vm_settings['name'], '--ram', str(ram), '--disk',
                         'path=' + default_memory_path + vm_settings['name'] + '.img,size=' + memory_size,
                         '--vcpus', str(cores), '--vnc', '-c', vm_settings['iso_path']])

    @staticmethod
    def destroy_vm(machine_name):
        try:
            machine = connection.lookupByName(machine_name)
            machine.undefine()
        except libvirt.libvirtError:
            raise ValueError("The machine to be deleted does not exist")


