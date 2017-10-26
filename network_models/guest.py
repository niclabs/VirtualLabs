import subprocess
import nic
from resources.template import Template
from parsers.guest_parser import GuestParser


class Guest:
    def __init__(self, info, nics):
        self.name = info['name']
        self.template = Template(info['type'], info['template_id'])
        self.nics = nics

    def create_guest(self):
        subprocess.call(['virt-clone', '--connect', 'qemu:///system',
                         '--original', self.template.name, '--name', self.name,
                         '--file', '/var/lib/libvirt/images/' + self.name + '.qcow2'])

    def power_on(self):
        subprocess.call(['virsh', 'start', self.name])

    def power_off(self):
        subprocess.call(['virsh', 'shutdown', self.name])

    def force_stop(self):
        subprocess.call(['virsh', 'destroy', self.name])

    def get_nic(self, nic_id):
        return self.nics[int(nic_id)]

    def add_nic(self, name, mac=0):
        nic_info = {'name': name, 'mac': mac}
        self.nics.append(nic.NIC(nic_info))

    def list_nics(self):
        return self.nics

    def delete_guest(self):
        self.force_stop()
        subprocess.call(['virsh', 'undefine', self.name])
        subprocess.call(['virsh', 'vol-delete', '--pool', 'default',
                         '/var/lib/libvirt/images/' + self.name + '.qcow2'])

    def connect_to_other(self, id_other, nic_name):
        pass





