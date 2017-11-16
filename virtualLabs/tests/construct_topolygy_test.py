import virtualLabs.network_models.network as n

net = n.Network()
net.create_from_xml("example_xmls/simple_net.xml")
net.to_xml()
