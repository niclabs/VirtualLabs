import virtualLabs.network_models.switch as switch
import virtualLabs.network_models.terminal as terminal
import virtualLabs.network_models.router as router

""" Lists all available guest types"""
guests_types = {
        'terminal': terminal.Terminal,
        'router': router.Router,
        'switch': switch.Switch
}


def create_guest_by_type(guest, guest_type, lab_name):
    """ Creates a specific guest instance from the guest information and the guest type
    :param guest: Dictionary with the guest information
    :param guest_type: Type of guest (most be one from the guest_types list)
    :param lab_name: Name of the laboratory this guest will belong to
    :return New guest instance"""
    return guests_types[guest_type](lab_name, guest)
