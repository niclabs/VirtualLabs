import subprocess
from virtualLabs.network_models.nics import NICs
import nic
from virtualLabs.resources.template import Template, NullTemplate


class Guest:
    """ Models a guest (a machine) of a network. Each guest has an associated virtual machine which this class also
    controls.
    Attributes:
        name(str): Name of the guest
        template(Template): Machine used as a base for this guest
        nics(list): List of the interfaces of the guest
    """
    def __init__(self, lab_name, info):
        """
        :param lab_name: Name of the laboratory this guest belongs to
        :param info: Information about the guest
        """
        self.name = lab_name + "_" + info['name']

        if 'template' in info:
            self.template = Template(info['type'], info['template'])
        else:
            self.template = NullTemplate()
        self.nics = NICs(info['nics']).create_nics()

    def get_name(self):
        """
        :return: Name of the guest
        """
        return self.name

    def create_guest(self):
        """ Creates the virtual machine that belongs to the guest """
        if not self.template.is_null():
            p = subprocess.Popen(['virt-clone', '--connect', 'qemu:///system',
                                  '--original', self.template.name, '--name', self.name,
                                  '--file', '/var/lib/libvirt/images/' + self.name + '.qcow2'])
            p.wait()


    def power_on(self):
        """ Turns on the guest virtual machine"""
        subprocess.call(['virsh', 'start', self.name])

    def type(self):
        """ Type of guest"""
        pass

    def power_off(self):
        """ Turns off nicely the virtual machine """
        subprocess.call(['virsh', 'shutdown', self.name])

    def force_stop(self):
        """Forces the machine to turn off """
        subprocess.call(['virsh', 'destroy', self.name])

    def get_nic(self, nic_id):
        """
        :param nic_id: Nic id
        :return: Nic of given id
        """
        return self.nics[int(nic_id)]

    def add_nic(self, name, mac=0):
        """ Adds a new NIC to the guest
        :param name: Name of the NIC
        :param mac: Optional. MAC address of the NIC
        """
        nic_info = {'name': name, 'mac': mac}
        self.nics.append(nic.NIC(nic_info))

    def list_nics(self):
        """
        :return: All NICs of the guest
        """
        return self.nics

    def delete_guest(self):
        """ Cleans up all resources associated to this guest, effectively removing it from the network"""
        self.force_stop()
        subprocess.call(['virsh', 'undefine', self.name])
        subprocess.call(['virsh', 'vol-delete', '--pool', 'default',
                         '/var/lib/libvirt/images/' + self.name + '.qcow2'])

    def to_dict(self):
        """ Fills a dictionary with the guest information so that it can be saved in an XML file
        :return: Dictionary with the guest information
        """
        dic = {'guest': {
            '@id': 0,
            '@type': self.type(),
            'name': self.name,
            'nics': []}
        }

        for n in self.nics:
            dic['guest']['nics'].append(n.to_dict())

        return dic




