import templates
from machines import Machines
from noncollisionmacs import NonCollisionMacGenerator

""" Defines a list of resources that are required for the laboratory creation 
and management"""
machines = Machines()
interfaces = NonCollisionMacGenerator(machines.get_all_machines_macs())
os_templates = templates.OSTemplates()
router_templates = templates.RouterTemplates()
switch_templates = templates.SwitchTemplates()

