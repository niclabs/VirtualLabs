from pynetlinux import brctl
import subprocess


class LinuxBridge:
    """ Models a linux bridge, managing its associated interfaces and using netem to set
    properties.
    Attributes:
        name (str): name of the bridge
        bridge(Bridge): instance representing the bridge
    """
    def __init__(self, name):
        """
        :param name: Name of the bridge
        """
        self.name = name
        self.bridge = brctl.addbr(self.name)
        subprocess.call(['tc', 'qdisc', 'add', 'dev', self.name, 'root', 'netem'])

    def add_interface(self, interface):
        """ Adds an interface to the bridge
        :param interface: Name of the interface
        """
        self.bridge.addif(interface)

    def remove_interface(self, interface):
        """ Removes an interface from the bridge
        :param interface: Name of the interface
        """
        self.bridge.delif(interface)

    def destroy_bridge(self):
        """ Deletes the bridge from the OS """
        self.bridge.delete()

    def cleanup_bridge(self):
        """Cleans up all changes on the bridge"""
        subprocess.call(['tc', 'qdisc', 'del', 'dev', self.name, 'root'])

    def qdisc_array(self):
        """ Creates an array with the keywords to apply a change using netem"""
        return ['tc', 'qdisc', 'change', 'dev', self.name, 'root', 'netem']

    def add_delay(self, delay_dic):
        """ Adds delay to the bridge
        :param delay_dic: Dictionary with the delay information
        """
        if delay_dic:
            command = self.qdisc_array() + ['delay', str(delay_dic['value']), str(delay_dic['random_variation']),
                                            str(delay_dic['correlation'])]
            if delay_dic['dist']:
                command += ['distribution', str(delay_dic['distribution'])]

            subprocess.call(command)

    def remove_delay(self):
        """ Removes the delay from the bridge (sets it as zero)"""
        self.add_delay({'value': 0})

    def add_loss(self, loss_dic):
        """ Adds loss to the bridge
        :param loss_dic: Dictionary with the loss information
        """
        if loss_dic:
            command = self.qdisc_array() + ['loss', str(loss_dic['value']), str(loss_dic['ran'])]
            subprocess.call(command)

    def remove_loss(self):
        """Remove the setted loss from the bridge"""
        self.add_loss({'value': 0})

    def add_duplication(self, dup):
        """ Adds packet duplication to the bridge
        :param dup: value of the duplication probability
        """
        command = self.qdisc_array() + ['duplicate', str(dup)]
        subprocess.call(command)

    def remove_duplication(self):
        """ Removes the packet duplication from the bridge"""
        self.add_duplication(0)

    def add_corruption(self, corr):
        """ Adds packet corruption to the bridge
        :param corr: value of the probability of corruption
        """
        command = self.qdisc_array() + ['corrupt', str(corr)]
        subprocess.call(command)

    def remove_corruption(self):
        """ Removes packet corruption from the bridge"""
        self.add_corruption(0)

    def add_gap_reordering(self, gap_dic):
        if gap_dic:
            command = self.qdisc_array() + ['gap', str(gap_dic['packet']), 'delay', str(gap_dic['delay'])]
            subprocess.call(command)

    def remove_gap_reordering(self):
        pass

    def add_reordering(self, reor_dic):
        if reor_dic:
            command = self.qdisc_array() + ['delay', str(reor_dic['delay']), 'reorder', str(reor_dic['probability']),
                                            str(reor_dic['correlation'])]
            subprocess.call(command)

    def remove_reordering(self):
        self.add_reordering({'delay': 0})

    def add_max_bandwidth(self, bandwidth_dic):
        subprocess.call(['wondershaper', self.name, bandwidth_dic['down'], bandwidth_dic['up']])

    def reset_bandwidth(self):
        subprocess.call(['wondershaper', 'clear', self.name])






