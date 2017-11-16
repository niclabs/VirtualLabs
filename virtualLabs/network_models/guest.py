import subprocess
from virtualLabs.network_models.nics import NICs
import nic
from virtualLabs.resources.template import Template, NullTemplate


class Guest:
    def __init__(self, lab_name, info):
        self.name = lab_name + "_" + info['name']

        if 'template' in info:
            self.template = Template(info['type'], info['template'])
        else:
            self.template = NullTemplate()
        self.nics = NICs(info['nics']).create_nics()

    def create_guest(self):
        if not self.template.is_null():
            subprocess.call(['virt-clone', '--connect', 'qemu:///system',
                             '--original', self.template.name, '--name', self.name,
                             '--file', '/var/lib/libvirt/images/' + self.name + '.qcow2',
                             '--check', 'path_exists=off'])

    def power_on(self):
        subprocess.call(['virsh', 'start', self.name])

    def type(self):
        pass

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

    def to_dict(self):
        dic = {'guest': {
            '@id': 0,
            '@type': self.type(),
            'name': self.name,
            'nics': []}
        }

        for n in self.nics:
            dic['guest']['nics'].append(n.to_dict())

        return dic




