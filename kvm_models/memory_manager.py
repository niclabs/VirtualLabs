from main import connection
from vm_defaults import *
from checkers.memory_checker import MemoryChecker
import subprocess


class MemoryManager:
    def __init__(self, pool=default_memory_pool):
        self.pool = connection.storageLookup(pool)
        self.memory_checker = MemoryChecker(self.list_memories())

    def create_volume(self, settings):
        self.memory_checker.check_memory(settings)
        path_to_memory = default_memory_path + settings['name'] + '.' + memory_format
        if 'size' in settings:
            size = settings['size']
        else:
            size = default_memory_size

        subprocess.call(['qemu-img', 'create', '-f', memory_format, path_to_memory, size])
        return path_to_memory

    def list_memories(self):
        return self.pool.listVolumes()

