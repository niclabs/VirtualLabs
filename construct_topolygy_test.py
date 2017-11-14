import network_models.network as n

net = n.Network()
net.create_from_xml("xmls/simple_net.xml")
net.to_xml()
