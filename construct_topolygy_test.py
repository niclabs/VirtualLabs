import network_models.network as n

net = n.Network()
net.load_from_xml("xmls/simple_net.xml")
net.construct_topology()