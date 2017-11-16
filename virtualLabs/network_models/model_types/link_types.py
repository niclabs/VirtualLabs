import network_models.external_link as external

import virtualLabs.network_models.guest_link as guest

link_types = {
    'internal': guest.GuestLink,
    'external': external.ExternalLink
}


def create_link_from_type(lab_name, link_id, info, guests, guest_checker):
    return link_types[info['type']](lab_name, link_id, info, guests, guest_checker)