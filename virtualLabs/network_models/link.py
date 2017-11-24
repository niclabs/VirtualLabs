import copy
import os
import subprocess
import xmltodict as xd
import endpoint
import virtualLabs.linux.bridge as br
import virtualLabs.linux.linux_utils


class Link:
    """ Model an abstract link in a network.
    Attributes:
        id(int): Id number of the link
        settings(dict): Dictionary with the properties of the link
        endpoints(list): endpoint(s) of the link
        bridge: Bridge instance that represents the link at a low-level
    """
    def __init__(self, link_id, link_info, guests, guest_checker, bridge_name):
        self.id = link_id

        if 'settings' in link_info:
            self.settings = link_info['settings']
        else:
            self.settings = {}

        self.endpoints = []

        for end in link_info['endpoints']:
            self.endpoints.append(endpoint.Endpoint(end, guests, guest_checker))

        self.bridge = br.LinuxBridge(bridge_name)
        self.initialize_parameters()

    def write_endpoint_xml(self, i):
        """ Write in a file the XML required to attach the link to a guest
        :param i: Index of the endpoint
        :return: The name of the file where the XML was written
        """
        xml = {'interface': {
            '@type': 'bridge',
            'source': {
                '@bridge': self.bridge.name
            },
            'model': {
                '@ type': 'virtio'
            },
            'alias': {
                '@name': ''
            },
            'mac': {
                '@address': ''
            }
        }}

        xml_end = copy.deepcopy(xml)

        xml_end['interface']['alias']['@name'] = self.endpoints[i].nic['name']
        xml_end['interface']['mac']['@address'] = self.endpoints[i].nic['mac']

        filename = 'interface_host.xml'
        xml_file = virtualLabs.linux.linux_utils.touch(filename)
        xd.unparse(xml_end, xml_file, pretty=True)
        xml_file.close()

        return filename

    def connect_guest(self, i):
        """ Attaches the nic to the guest and to the bridge representing the link
        :param i: Index of the endpoint to connect
        """
        filename = self.write_endpoint_xml(i)
        self.attach_idevice(filename, self.endpoints[i].guest.name)

    @staticmethod
    def attach_idevice(xml_name, guest_name):
        """ Attaches a device to a guest
        :param xml_name: Name of the file containing the device XML
        :param guest_name:
        """
        subprocess.call(['virsh', 'attach-device', guest_name, '--config', xml_name])
        os.remove(xml_name)

    def clean_up(self):
        """ Deletes the resources (the bridge) associated to this link """
        subprocess.call(['brctl', 'delbr', self.bridge.name])

    def detach_link(self, index):
        """ Detaches the device (hence, disconnecting) from a guest
        :param index: Index of the endpoint to select
        """
        filename = self.write_endpoint_xml(index)
        subprocess.call(['virsh', 'detach-device', self.endpoints[index].guest.name, '--persistent', filename])
        os.remove(filename)

    def initialize_parameters(self):
        """ Sets all desired properties on the link """
        if 'reordering' in self.settings:
            self.bridge.add_reordering(self.settings['reordering'])

        if 'delay' in self.settings:
            self.bridge.add_delay(self.settings['delay'])

        if 'loss' in self.settings:
            self.bridge.add_loss(self.settings['loss'])

        if 'gap' in self.settings:
            self.bridge.add_gap_reordering(self.settings['gap'])

        if 'corruption' in self.settings:
            self.bridge.add_corruption(self.settings['corruption'])

        if 'duplication' in self.settings:
            self.bridge.add_duplication(self.settings['duplication'])

        if 'bandwidth' in self.settings:
            self.bridge.add_max_bandwidth(self.settings['bandwidth'])

    def link_condition(self):
        pass

    def clean_link(self):
        """Deletes all set properties of the link"""
        self.bridge.cleanup_bridge()

    def to_dict(self):
        """ Creates a dictionary with this link information, so that it can be saved
        :return: Dictionary summarizing this link
        """
        dic = {'settings': self.settings,
               'endpoints': []}

        for e in self.endpoints:
            dic['endpoints'].append({'endpoint': e.to_dict()})

        return dic


