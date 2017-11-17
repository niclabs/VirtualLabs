class VirtualMachineChecker:
    """ In charge of checking the consistency of the parameters for a virtual machine
    """
    def __init__(self):
        pass

    def check_vm(self, vm):
        """ Checks the completitude of the data used to create a virtual machine
        :param vm: Dictionary with the data of the virtual machine
        """
        if 'name' not in vm:
            raise ValueError("Can not create a virtual machine without a name")

        if 'iso_path' not in vm:
            raise ValueError("Can not create a virtual machine without an iso image")

