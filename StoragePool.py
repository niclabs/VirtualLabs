import libvirt
import xmltodict


class MemoryManager:
    def __init__(self, path):
        self.connection = libvirt.open("qemu:///system")
        self.path = path

    def create_storage_pool(self, name, capacity=100000000000):
        xml = {}
        xml['pool']['@type'] = 'dir'
        xml['pool']['name'] = self.path
        xml['pool']['capacity'] = capacity
        xml['pool']['capacity']['@unit'] = 'bytes'
        xml['pool']['allocation'] = 237457858
        xml['pool']['allocation']['@unit'] = 'bytes'

        xml['pool']['target']['path'] = name
        xml['pool']['target']['permissions']['mode'] = 0755
        xml['pool']['target']['permissions']['owner'] = -1
        xml['pool']['target']['permissions']['group'] = -1

        xml_storage = xmltodict.unparse(xml)

        pool = self.connection.storagePoolDefineXML(xml_storage, 0)

        pool.setAutostart(1)
        return StoragePool(pool)

    def get_storage_pool_by_name(self, name):
        pool = self.connection.storagePoolLookupByName(name)
        return StoragePool(pool)

    def list_all_storage_pools(self):
        pools = self.connection.listAllStoragePools(0)
        return list(map((lambda p: StoragePool(p)), pools))


class StoragePool:
    def __init__(self, pool):
        self.pool = pool
        self.valid = True

    def create_storage_volume(self, path, name, capacity):
        xml = {}
        xml['volume']['name'] = name + '.img'
        xml['volume']['allocation']['@unit'] = 'G'
        xml['volume']['allocation'] = capacity
        xml['volume']['capacity']['@unit'] = 'G'
        xml['volume']['capacity'] = capacity
        xml['volume']['target']['path'] = path + name + '.img'
        xml['volume']['target']['format']['@type'] = 'qcow2'
        xml['volume']['target']['permissions']['owner'] = 107
        xml['volume']['target']['permissions']['group'] = 107
        xml['volume']['target']['permissions']['mode'] = 0744
        xml['volume']['target']['permissions']['label'] = 'virt_image_t'

        volume_xml = xmltodict.unparse(xml)

        vol = self.pool.createXML(volume_xml, 0)
        return StorageVolume(vol)

    def delete_pool(self):
        self.pool.undefine()
        self.valid = False

    def is_valid(self):
        return self.valid

    def list_volumes(self):
        volumes = self.pool.listVolumes()
        return list(map((lambda v: StorageVolume(self.pool.storageVolLookupByName(v))), volumes))


class StorageVolume:
    def __init__(self, volume):
        self.vol = volume
        self.valid = True

    def delete_volume(self):
        self.vol.wipe(0)
        self.vol.delete(0)
        self.valid = False

    def clone(self, name):
        print("This can take a long time...")

        path = self.vol.path()
        index = path.rfind('\\')
        real_path = path[:-index]

        info = self.get_info()

        xml = {}
        xml['volume']['name'] = name + '.img'
        xml['volume']['allocation']['@unit'] = 'G'
        xml['volume']['allocation'] = info['allocation']
        xml['volume']['capacity']['@unit'] = 'G'
        xml['volume']['capacity'] = info['capacity']
        xml['volume']['target']['path'] = real_path + name + '.img'
        xml['volume']['target']['format']['@type'] = 'qcow2'
        xml['volume']['target']['permissions']['owner'] = 107
        xml['volume']['target']['permissions']['group'] = 107
        xml['volume']['target']['permissions']['mode'] = 0744
        xml['volume']['target']['permissions']['label'] = 'virt_image_t'

        stg_xml = xmltodict.unparse(xml)

        stgvol2 = self.pool.createXMLFrom(stg_xml, self.vol, 0)

        return StorageVolume(stgvol2)

    def get_info(self):
        info = self.vol.info()
        return {'capacity': str(info[1]), 'allocation': str(info[2])}




