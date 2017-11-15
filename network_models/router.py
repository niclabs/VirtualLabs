import guest


class Router(guest.Guest):
    def __init__(self, lab_name, os_info):
        guest.Guest.__init__(self, lab_name, os_info)

    def type(self):
        return 'router'
