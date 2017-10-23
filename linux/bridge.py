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

    def cleanup_bridge(self):
        subprocess.call(['tc', 'qdisc', 'del', 'dev', self.name, 'root'])

    def qdisc_array(self):
        return ['tc', 'qdisc', 'change', 'dev', self.name, 'root', 'netem']

    def add_delay(self, delay, ran_var=0, correlation=0):
        command = self.qdisc_array() + ['delay', delay, ran_var, correlation]
        subprocess.call(command)

    def remove_delay(self):
        self.add_delay(0)

    def add_loss(self, loss, ran_var=0):
        command = self.qdisc_array() + ['loss', loss, ran_var]
        subprocess.call(command)

    def remove_loss(self):
        self.add_loss(0)

    def add_duplication(self, dup):
        command = self.qdisc_array() + ['duplicate', dup]
        subprocess.call(command)

    def remove_duplication(self):
        self.add_duplication(0)

    def add_corruption(self, corr):
        command = self.qdisc_array() + ['corrupt', corr]
        subprocess.call(command)

    def remove_corruption(self):
        self.add_corruption(0)

    def add_gap_reordering(self, index, delay):
        command = self.qdisc_array() + ['gap', index, 'delay', delay]
        subprocess.call(command)

    def remove_gap_reordering(self):
        pass

    def add_reordering(self, delay, prob=0, corr=0):
        command = self.qdisc_array() + ['delay', delay, 'reorder', prob, corr]
        subprocess.call(command)

    def remove_reordering(self):
        self.add_reordering(0)

    def add_max_bandwidth(self):
        pass

    def reset_bandwidth(self):
        pass





