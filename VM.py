import libvirt

class VirtualMachine:
    def __init__(self, name):
        self.connection = libvirt.open('qemu:///system')
        self.name = name

    def define_xml(self, path_to_iso, path_to_image):
        xmlVM = """
    <domain type="kvm">  
        <name>"""+name+"""</name>
        <cpu>
            <topology cores="4" sockets="1" threads="4" />
        </cpu>
        <memory unit="MB">512</memory>
        <currentMemory unit="MB">512</currentMemory>
        <vcpu placement="static">1</vcpu>
        <os>
            <type>hvm</type>
            <boot dev="hd" />
        </os>
        <features>
            <acpi />
            <apic />
            <pae />
        </features>
        <clock offset="utc" />
        <on_poweroff>destroy</on_poweroff>
        <on_reboot>restart</on_reboot>
        <on_crash>restart</on_crash>
        <devices>
            <emulator>/usr/libexec/qemu-kvm</emulator>
            <disk device="disk" type="file">
                <driver cache="none" name="qemu" type="raw" />
                <source file='"""+path_to_image+"""' />
                <target dev="hda" />
                <address bus="0" controller="0" target="0" type="drive" unit="0" />
            </disk>
            <disk device="cdrom" type="file">
                <source file='"""+path_to_iso+"""' />
                <driver name="qemu" type="raw" />
                <target bus="ide" dev="hdc" />
                <readyonly />
                <address bus="1" controller="0" target="0" type="drive" unit="0" />
            </disk>
            <interface type="bridge">
                <source network="br0" />
            </interface>
            <graphics port="-1" type="vnc" />
        </devices>
    </domain>"""

        text_file = open(self.name+".xml", "w")
        text_file.write(xmlVM)
        text_file.close()

    def create(self, path_to_xml):
        xml = ""
        with open(path_to_xml, "r") as file:
            xml = file.read()

        machine = self.connection.defineXML(xml)
        return machine

    def destroy(self):
        try:
            machine = self.connection.lookupByName(self.name)
            machine.undefine()
        except libvirt.libvirtError, e:
            print("La maquina pedida no existe")
        

    