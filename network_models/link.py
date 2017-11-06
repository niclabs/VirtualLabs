import linux.bridge as br
import endpoint
import subprocess
import xmltodict as xd
import copy
import linux.linux_utils
import os
import parsers.link_info_parser as lp


class Link:
    def __init__(self, link_id, link_info, guests):
        self.id = link_id
        self.settings = link_info['settings']
        self.endpoints = []

        for end in link_info['endpoints']:
            self.endpoints.append(endpoint.Endpoint(end, guests))

        self.bridge = br.LinuxBridge("link" + str(self.id))
        self.initialize_parameters()

    def connect_guests(self):
        self.connect_guest(0)
        self.connect_guest(1)

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
        xml_file = linux.linux_utils.touch(filename)
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

    def destroy_link(self):
        self.detach_link(0)
        self.detach_link(1)
        self.clean_up()

    def detach_link(self, index):
        filename = self.write_endpoint_xml(index)
        subprocess.call(['virsh', 'detach-device', self.endpoints[index].guest.name, '--persistent', filename])
        os.remove(filename)

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
