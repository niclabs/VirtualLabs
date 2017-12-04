# VirtualLabs

The VirtualLabs project is an API for the generation and management
of virtual laboratories for teaching and research in networks. It allows the creation
of several virtual network devices (switches, routers, computers, etc), that can be connected
as required to simulate all kinds of real life situations. Besides, it is left
open for further extensions.

VirtualLab is completely based on open source software. It uses QEMU/KVM virtual machines to simulate independent machines,
and the standard linux bridge utilities to connect them. Switching utilities are provided using LISA (LInux Switching Appliance),
while routing comes from VyOs, a fork of the Vyatta project. Most of the virtual machine creation and manipulation comes from libvirt and virsh calls.

VirtualLab comes with a number of pre installed operating system templates that can be used to create guest machines for custom laboratories
or topologies, plus a set of ready-to-use preconfigured labs that illustrate the use and configuration of a virtual lab.

Visit our [wiki](https://github.com/niclabs/VirtualLabs/wiki) for installation and usage instructions.
