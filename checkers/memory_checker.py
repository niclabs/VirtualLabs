class MemoryChecker:
    def __init__(self, memory_list):
        self.memory_list = memory_list

    def check_memory(self, memory):
        if 'name' not in memory:
            raise ValueError()
