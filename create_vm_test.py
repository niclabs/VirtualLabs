import kvm_models.vm_manager as vm

manager = vm.VirtualMachineManager()
settings = {'name': 'ubuntu', 'ram': 1024, 'cores': 2, 'iso_path': '/home/cata/images/ubuntu.iso'}
manager.create_new_vm(settings)

