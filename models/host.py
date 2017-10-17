import nic
import templates
import subprocess


class Host:
    def __init__(self, os_info):
        self.name = os_info['name']
        self.template = templates.Template(os_info['@id'])
        self.nics = []
        for n in os_info['nics']['nic']:
            self.nics.append(nic.NIC(n))

    def create_host(self):
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

    def list_nics(self):
        return self.nics

    def delete_host(self):
        self.force_stop()
        subprocess.call(['virsh', 'undefine', self.name])
        subprocess.call(['virsh', 'vol-delete', '--pool', 'default',
                         '/var/lib/libvirt/images/' + self.name + '.qcow2'])

    def connect_to_other(self, id_other, nic_id):
        pass



