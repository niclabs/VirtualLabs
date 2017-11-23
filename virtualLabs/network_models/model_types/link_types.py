import virtualLabs.network_models.external_link as external
import virtualLabs.network_models.guest_link as guest
from virtualLabs.config.default_values import default_link_type

"""List of the available link types"""
link_types = {
    'internal': guest.GuestLink,
    'external': external.ExternalLink
}


def create_link_from_type(lab_name, link_id, info, guests, guest_checker):
    """ Creates a link that will be added to the network
    :param lab_name: Name of the laboratory this link will belong to
    :param link_id: Id to assign to the link
    :param info: Information abou the link
    :param guests: List of guests of the network
    :param guest_checker: GuestChecker instances used to check the guests to connect
    :return: The created Guest instance
    """
    link_type = info['type'] if 'type' in info else default_link_type
    return link_types[link_type](lab_name, link_id, info, guests, guest_checker)
