from virtualLabs import kvm_models as vm

manager = vm.VirtualMachineManager()
settings = {'name': 'ubuntu', 'ram': 2048, 'cores': 2, 'iso_path': '/home/cata/images/ubuntu.iso'}
manager.create_new_vm(settings)

