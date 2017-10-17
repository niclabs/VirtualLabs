from pynetlinux import brctl


class LinuxBridge:
    def __init__(self, name):
        self.name = name
        self.bridge = brctl.addbr(self.name)

    def add_interface(self, interface):
        self.bridge.addif(interface)

    def remove_interface(self, interface):
        self.bridge.delif(interface)

    def destroy_bridge(self):
        self.bridge.delete()

    def add_delay(self, delay):
        pass

    def remove_delay(self):
        pass

    def add_loss(self, loss):
        pass

    def remove_loss(self):
        pass

    def add_duplication(self, dup):
        pass

    def remove_duplication(self):
        pass

    def add_reordering(self, reord):
        pass

    def remove_reordering(self):
        pass

    def








