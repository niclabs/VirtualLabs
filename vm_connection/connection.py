import libvirt


class Connection:
    def __init__(self):
        self.connection = libvirt.open("qemu:///system")

    def list_machines(self):
        return self.connection.listDefinedDomains()



