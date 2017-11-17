import libvirt
import subprocess

from virtualLabs import connection
from virtualLabs.checkers.vm_checker import VirtualMachineChecker
from vm_defaults import *


class VirtualMachineManager:
    """ In charge of managing the creation and destruction of virtual machines
    Attributes:
        vm_checker (VirtualMachineChecker): Instance of the class that checks the correctitude of the data used
                                            to create the VM
    """
    def __init__(self):
        self.vm_checker = VirtualMachineChecker()

    def create_new_vm(self, vm_settings):
        """ Creates a new virtual machine (not from a template, but from an image file)
        :param vm_settings: Settings for the new virtual machine
        """
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
        """ Deletes a virtual machine
        :param machine_name: Name of the machine to delete
        """
        try:
            machine = connection.lookupByName(machine_name)
            machine.undefine()
        except libvirt.libvirtError:
            raise ValueError("The machine to be deleted does not exist")


