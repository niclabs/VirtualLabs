import libvirt


class Connection:
    """ Libvirt wrapper class, that simplifies names and eliminates the need to know about libvirt
    Attributes:
        connection(libvirt.Connection): Connection to the qemu daemon
    """
    def __init__(self):
        self.connection = libvirt.open("qemu:///system")

    def list_machines(self):
        """
        :return: Names of the virtual machines defined in the host
        """
        return self.connection.listDefinedDomains()

    def lookupByName(self, name):
        """
        :param name: Name of the machine to obtain
        :return: Virtual machine of the given name
        """
        return self.connection.lookupByName(name)



