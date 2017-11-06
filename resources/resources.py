from noncollisionmacs import NonCollisionMacGenerator
from machines import Machines
import templates

machines = Machines()
interfaces = NonCollisionMacGenerator(machines.get_all_machines_macs())
os_templates = templates.OSTemplates()
router_templates = templates.RouterTemplates()
switch_templates = templates.SwitchTemplates()

