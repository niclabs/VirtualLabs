import models.network as net

simple_net = net.Network()
simple_net.load_from_xml("xmls/simple_net.xml")
simple_net.construct_topology()

simple_net.show_links()
