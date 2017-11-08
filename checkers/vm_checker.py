class VirtualMachineChecker:
    def __init__(self):
        pass

    def check_vm(self, vm):
        if 'name' not in vm:
            raise ValueError("Can not create a virtual machine without a name")

        if 'iso_path' not in vm:
            raise ValueError("Can not create a virtual machine without an iso image")

