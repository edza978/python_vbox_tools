# python_vbox_tools
Python tool aimed to help in VBox VMs creation using vboxmanage commands.
This tools uses only vboxmanage's commands, so it works in Windows, Linux and every operating system with VirtualBox's console

## Arguments / Options
```
usage: createvm.py [-h] [-cpus CPU] [-hi HI] [-sata] [-ide] [-vrde] [-vp VP]
                   [-iso ISO] [-vdis VDIS] [-hds HDD] [-vdi VDI]
                   name ostype ram

=> VirtualBox VM Creator <=
optional arguments:
  -h, --help            show this help message and exit

Required/Requerido:
  name                  VM Name/Nombre
  ostype                VM's OS Type / Tipo de sistema operativo
                        (list/lista: vboxmanage list ostypes)
  ram                   VM's RAM (MBs)/Cantidad de RAM

Others/Otros:
  -cpus CPU, --cpus CPU
                        VM's Cores / Cantidad n├║cleos
  -hi HI, --hostonly-if HI
                        HostOnly IF's name / Nombre interface HostOnly.
                        (list/lista: vboxmanage list hostonlyifs)
  -sata, --sata         Create SATA bus / Crear bus SATA. Default: True
  -ide, --ide           Create IDE bus / Crear bus IDE. Default: True

Remote Access/Acceso Remoto:
  -vrde, --enable-vrde  Allow remote desktop to this VM / Permitir
                        escritorio remoto a esta VM. Default: False
  -vp VP, --vrde-port VP
                        VRDE Port for this VM / Puerto para VRDE a esta VM.
                        Default: 3389

Extra files/ Archivos extra:
  -iso ISO, -iso-file ISO
                        ISO image file / Imagen ISO
  -vdis VDIS, --vdi-folder VDIS
                        VDI's storage path/ Ruta almacenamiento VDIs
  -hds HDD, --hdd-size HDD
                        VM's HDD size (MBs)/ Espacio en Disco
  -vdi VDI, --hdd-vdi VDI
                        VM VDI file (If not defined, will be created with
                        same name than VM) / Archivo VDI (Si no se especifica,
                        se creara uno con el mismo nombre de la VM).
```
### Examples

##### Create VM in Linux with 1GB RAM and existing VDI:
python createvm.py myvm Ubuntu_64 1024 -cpus 2 -hds 8192 -vdi $HOME/vdis/myvm.vdi -iso $HOME/ubuntu.iso

##### Create VM in Windows with 512MB RAM and new VDI of 1GB:
python createvm.py test Ubuntu_64 512 -vdis d:\VDIs -hds 1024
