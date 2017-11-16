from link import Link


class GuestLink(Link):
    def __init__(self, lab_name, link_id, link_info, guests, guest_checker):
        bridge_name = lab_name + "_link" + str(self.id)
        Link.__init__(link_id, link_info, guests, guest_checker, bridge_name)

    def connect_guests(self):
        self.connect_guest(0)
        self.connect_guest(1)

    def destroy_link(self):
        self.detach_link(0)
        self.detach_link(1)
        self.clean_up()
