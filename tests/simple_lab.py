from virtualLabs.lab.laboratory import Laboratory

lab = Laboratory()
lab.name_laboratory("simple_lab")
net = lab.get_topology()

guest1 = {
    'name':'pc1',
    'type': 'terminal',
    'template': {'name': 'template_os_debian'},
    'nics': [{}]
}

guest2 = {
    'name': 'pc2',
    'type': 'terminal',
    'template': {'name': 'template_os_debian'},
    'nics': [{}]
}

router = {
    'name': 'router',
    'type': 'router',
    'template': {'id': 0},
    'nics': [{},{}]
}

link1 = {
    'endpoints': [{'guest': {'name': 'pc1'}, 'nic': {'id': 0}},
                  {'guest': {'name': 'router'}, 'nic': {'id': 0}}]
}

link2 = {
    'endpoints': [{'guest': {'name': 'pc2'}, 'nic': {'id': 0}},
                  {'guest': {'name': 'router'}, 'nic': {'id': 1}}]
}

net.create_guest(guest1)
net.create_guest(guest2)
net.create_guest(router)

net.create_link(link1)
net.create_link(link2)

net.construct_topology()
net.turn_network_on()

