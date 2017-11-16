from virtualLabs.kvm_models.vm_defaults import memory_format


class MemoryChecker:
    def __init__(self, memory_list):
        self.memory_list = memory_list

    def check_memory(self, memory):
        if 'name' not in memory:
            raise ValueError("Can not create a memory volume without a name")

        complete_name = memory['name'] + '.' + memory_format

        if complete_name in self.memory_list:
            raise ValueError("Trying to override an existent memory volume")

        if 'size' in memory:
            if memory['size'][-1] is not 'G' and memory['size'][-1] is not 'M':
                raise ValueError("Unrecognized memory size")

        self.memory_list.append(complete_name)
