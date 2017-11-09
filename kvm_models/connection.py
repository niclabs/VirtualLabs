import libvirt


class Connection:
    def __init__(self):
        self.connection = libvirt.open("qemu:///system")

    def list_machines(self):
        return self.connection.listDefinedDomains()

    def lookupByName(self, name):
        return self.connection.lookupByName(name)

    def storageLookup(self, name):
        return self.connection.storagePoolLookupByName(name)

    def createFromXML(self, xml):
        return self.connection.defineXML(xml)


