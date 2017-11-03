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

    def add_delay(self, delay_dic):
        if delay_dic:
            command = self.qdisc_array() + ['delay', str(delay_dic['value']), str(delay_dic['ran']), str(delay_dic['corr'])]
            if delay_dic['dist']:
                command += ['distribution', str(delay_dic['dist'])]

            subprocess.call(command)

    def remove_delay(self):
        self.add_delay({'value': 0})

    def add_loss(self, loss_dic):
        if loss_dic:
            command = self.qdisc_array() + ['loss', str(loss_dic['value']), str(loss_dic['ran'])]
            subprocess.call(command)

    def remove_loss(self):
        self.add_loss({'value': 0})

    def add_duplication(self, dup):
        command = self.qdisc_array() + ['duplicate', str(dup)]
        subprocess.call(command)

    def remove_duplication(self):
        self.add_duplication(0)

    def add_corruption(self, corr):
        command = self.qdisc_array() + ['corrupt', str(corr)]
        subprocess.call(command)

    def remove_corruption(self):
        self.add_corruption(0)

    def add_gap_reordering(self, gap_dic):
        if gap_dic:
            command = self.qdisc_array() + ['gap', str(gap_dic['pac']), 'delay', str(gap_dic['delay'])]
            subprocess.call(command)

    def remove_gap_reordering(self):
        pass

    def add_reordering(self, reor_dic):
        if reor_dic:
            command = self.qdisc_array() + ['delay', str(reor_dic['delay']), 'reorder', str(reor_dic['prob']),
                                            str(reor_dic['corr'])]
            subprocess.call(command)

    def remove_reordering(self):
        self.add_reordering({'delay': 0})

    def add_max_bandwidth(self):
        pass

    def reset_bandwidth(self):
        pass





