import linux.bridge as br
import endpoint
import subprocess
import xmltodict as xd
import copy
import linux.linux_utils
import os
import parsers.link_info_parser as lp


class Link:
    def __init__(self, settings, link_info):
        self.settings = settings
        self.id = settings['@id']
        self.endpoints = []
        for end in settings['endpoints']['endpoint']:
            self.endpoints.append(endpoint.Endpoint(end, hosts))

        self.bridge = br.LinuxBridge("link"+self.id)
        self.initialize_parameters()

    def connect_hosts(self):
        self.connect_host(0)
        self.connect_host(1)

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

        host = self.endpoints[i].host

        xml_end['interface']['alias']['@name'] = host.get_nic(self.endpoints[i].nic).interface
        xml_end['interface']['mac']['@address'] = host.get_nic(self.endpoints[i].nic).mac_address

        filename = 'interface_host.xml'
        xml_file = linux.linux_utils.touch(filename)
        xd.unparse(xml_end, xml_file, pretty=True)
        xml_file.close()

        return filename

    def connect_host(self, i):
        filename = self.write_endpoint_xml(i)
        self.attach_idevice(filename, self.endpoints[i].host.name)

    @staticmethod
    def attach_idevice(xml_name, host_name):
        subprocess.call(['virsh', 'attach-device', host_name, '--config', xml_name])
        os.remove(xml_name)

    def clean_up(self):
        subprocess.call(['brctl', 'delbr', self.bridge.name])

    def hot_unplug(self, index):
        filename = self.write_endpoint_xml(index)
        subprocess.call(['virsh', 'detach-device', self.endpoints[index].host.name, '--persistent', filename])
        os.remove(filename)

    def hot_plug(self):
        pass

    def initialize_parameters(self):
        parser = lp.LinkInfoParser(self.settings)
        parameters = parser.get_all_parsed()

        self.bridge.add_reordering(parameters['reordering'])
        self.bridge.add_delay(parameters['delay'])
        self.bridge.add_loss(parameters['loss'])
        self.bridge.add_gap_reordering(parameters['gap'])
        self.bridge.add_corruption(parameters['corruption'])
        self.bridge.add_duplication(parameters['duplication'])

    def link_condition(self):
        pass

    def clean_link(self):
        self.bridge.cleanup_bridge()
