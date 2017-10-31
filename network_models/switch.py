import guest


class Switch(guest.Guest):
    def __init__(self, os_info):
        guest.Guest.__init__(self, os_info)

