from link import Link
from virtualLabs.config import host_config


class ExternalLink(Link):
    def __init__(self, lab_name, link_id, link_info, guests, guest_checker):
        bridge_name = host_config.host_bridge
        Link.__init__(link_id, link_info, guests, guest_checker, bridge_name)

    def connect_guests(self):
        self.connect_guest(0)

    def destroy_link(self):
        self.detach_link(0)
        self.clean_up()
