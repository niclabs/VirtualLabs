from guest import Guest


class Terminal(Guest):
    def __init__(self, os_info):
        Guest.__init__(os_info)
