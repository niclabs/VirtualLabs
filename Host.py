import subprocess


def maxCPUS(connection):
    vcpus = connection.getMaxVcpus(None)
    return vcpus


def clone_vm(to_clone, new_name):
    subprocess.call(['virt-clone', '--connect', 'qemu:///system',
                     '--original', to_clone, '--name', new_name,
                     '--file', '/var/lib/libvirt/images/'+new_name+'.qcow2'])


