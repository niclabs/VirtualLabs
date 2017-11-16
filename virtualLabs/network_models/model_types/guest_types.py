import network_models.switch as switch
import network_models.terminal as terminal

import virtualLabs.network_models.router as router

guests_types = {
        'terminal': terminal.Terminal,
        'router': router.Router,
        'switch': switch.Switch
}


def create_guest_by_type(guest, guest_type, lab_name):
    return guests_types[guest_type](lab_name, guest)
