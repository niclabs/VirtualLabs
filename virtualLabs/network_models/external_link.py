from link import Link
from virtualLabs.config import host_config


class ExternalLink(Link):
    def __init__(self, lab_name, link_id, link_info, guests, guest_checker):
        """
        :param lab_name: Laboratory this link belongs to
        :param link_id: Id of this link
        :param link_info: Information to create this link (settings and endpoints)
        :param guests: List of guests of the laboratory
        :param guest_checker: GuestChecker instance
        """
        bridge_name = host_config.host_bridge
        Link.__init__(self, link_id, link_info, guests, guest_checker, bridge_name)

    def connect_guests(self):
        """ Initializes the connection between the two endpoints"""
        self.connect_guest(0)

    def destroy_link(self):
        """Detaches the NICs on each endpoint and destroys the connection"""
        self.detach_link(0)
        self.clean_up()
