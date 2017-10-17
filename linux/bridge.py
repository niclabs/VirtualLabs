from pynetlinux import brctl
import subprocess


class LinuxBridge:
    def __init__(self, name):
        self.name = name
        self.bridge = brctl.addbr(self.name)
        subprocess.call(['tc', 'qdisc', 'add', 'dev', self.name, 'root', 'netem'])

    def add_interface(self, interface):
        self.bridge.addif(interface)

    def remove_interface(self, interface):
        self.bridge.delif(interface)

    def destroy_bridge(self):
        self.bridge.delete()

    def qdisc_array(self):
        return ['tc', 'qdisc', 'change', 'dev', self.name, 'root', 'netem']

    def add_delay(self, delay, ran_var=0, correlation=0):
        command = self.qdisc_array() + ['delay', delay, ran_var, correlation]
        subprocess.call(command)

    def remove_delay(self):
        self.add_delay(0)

    def add_loss(self, loss):
        command = self.qdisc_array() + ['loss', loss]
        subprocess.call(command)

    def remove_loss(self):
        self.add_loss(0)

    def add_duplication(self, dup):
        command = self.qdisc_array() + ['duplicate', dup]
        subprocess.call(command)

    def remove_duplication(self):
        self.add_duplication(0)

    def add_corruption(self, corr):
        pass

    def remove_corruption(self):
        self.add_corruption(0)

    def add_reordering(self, reord):
        pass

    def remove_reordering(self):
        pass









