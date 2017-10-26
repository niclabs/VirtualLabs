from resources.machines import Machines

machines = Machines()
mac = machines.get_macs('template_os_debian')
print mac