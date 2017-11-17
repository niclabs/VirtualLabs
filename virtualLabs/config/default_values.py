""" Default name for a guest's network cards"""
default_nic = 'eth'

""" Default name for the machines depending on their type """
default_machine = {
    'terminal': 'pc',
    'switch': 'sw',
    'router': 'rt'
}

""" Defualt type of guest if none is provided by the user """
default_type = 'terminal'

""" Default link type if none is provided by the user """
default_link_type = "internal"
