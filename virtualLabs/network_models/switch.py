import guest


class Switch(guest.Guest):
    """ Models a switch"""
    def __init__(self, lab_name, os_info):
        guest.Guest.__init__(self, lab_name, os_info)

    def type(self):
        return 'switch'

