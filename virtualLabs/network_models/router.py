import guest


class Router(guest.Guest):
    """Models a router"""
    def __init__(self, lab_name, os_info):
        guest.Guest.__init__(self, lab_name, os_info)

    def type(self):
        return 'router'
