from main import connection
from vm_defaults import *
from checkers.memory_checker import MemoryChecker


class MemoryManager:
    def __init__(self, pool=default_memory_pool):
        self.pool = connection.storagePoolLookupByName(pool)
        self.memory_checker = MemoryChecker(self.list_memories())

    def create_volume(self, settings):
        pass

    def list_memories(self):
        return self.pool.listVolumes()

