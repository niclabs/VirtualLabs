from virtualLabs.lab.laboratory import Laboratory

lab = Laboratory()
lab.name_laboratory("simple_net")
net = lab.get_topology()

net.create_from_xml("/example_xmls/simple_net.xml")

#net.construct_topology()
#net.turn_network_on()

lab.save_laboratory()