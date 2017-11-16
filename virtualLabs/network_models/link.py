import copy
import os
import subprocess
import xmltodict as xd
import endpoint
import virtualLabs.linux.bridge as br
import virtualLabs.linux.linux_utils


class Link:
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
        filename = self.write_endpoint_xml(i)
        self.attach_idevice(filename, self.endpoints[i].guest.name)

    @staticmethod
    def attach_idevice(xml_name, guest_name):
        subprocess.call(['virsh', 'attach-device', guest_name, '--config', xml_name])
        os.remove(xml_name)

    def clean_up(self):
        subprocess.call(['brctl', 'delbr', self.bridge.name])

    def detach_link(self, index):
        filename = self.write_endpoint_xml(index)
        subprocess.call(['virsh', 'detach-device', self.endpoints[index].guest.name, '--persistent', filename])
        os.remove(filename)

    def initialize_parameters(self):
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
        self.bridge.cleanup_bridge()

    def to_dict(self):
        dic = {'settings': self.settings,
               'endpoints': []}

        for e in self.endpoints:
            dic['endpoints'].append({'endpoint': e.to_dict()})

        return dic


