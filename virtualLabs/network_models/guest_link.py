from link import Link


class GuestLink(Link):
    """ Represents a link between two guests (an internal link) """
    def __init__(self, lab_name, link_id, link_info, guests, guest_checker):
        """
        :param lab_name: Laboratory this link belongs to
        :param link_id: Id of this link
        :param link_info: Information to create this link (settings and endpoints)
        :param guests: List of guests of the laboratory
        :param guest_checker: GuestChecker instance
        """
        Link.__init__(self, link_id, link_info, guests, guest_checker, lab_name + "_l" + str(link_id))

    def connect_guests(self):
        """ Initializes the connection between the two endpoints"""
        self.connect_guest(0)
        self.connect_guest(1)

    def destroy_link(self):
        """Detaches the NICs on each endpoint and destroys the connection"""
        self.detach_link(0)
        self.detach_link(1)
        self.clean_up()
