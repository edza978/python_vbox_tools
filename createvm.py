#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse      # Manejo de argumentos
import subprocess  # Ejecución de comandos

def print_error(msg):
    print("Error: %s" % msg)
    raise SystemExit()

def print_pass(msg,lst):
    print("Running pass: %s.\nCMD: %s" %(msg," ".join(lst)))

def createVM(args):
    # Store all commands
    cmds={}
    # Store order to run commands
    sortcmds=['cmd01','cmd02','cmd03']

    cmds["cmd01"]=['vboxmanage','createvm','--name',args.name,'--ostype',args.ostype,'--register' ]
    cmds["cmd02"]=['vboxmanage','modifyvm',args.name,'--boot1','dvd','--boot2','disk','--boot3','net','--biosbootmenu','messageandmenu']
    if(args.cpu):
        cmds["cmd03"]=['vboxmanage','modifyvm',args.name,'--memory',str(args.ram),'--cpus',str(args.cpu)]
    else:
        cmds["cmd03"]=['vboxmanage','modifyvm',args.name,'--memory',str(args.ram)]

    if(args.sata):
        cmds["cmd04"]=['vboxmanage','storagectl',args.name,'--name','sata0','--add','sata','--bootable','on','--sataportcount','2']
        sortcmds.append('cmd04')
    if(args.ide):
        cmds["cmd05"]=['vboxmanage','storagectl',args.name,'--name','ide0','--add','ide','--bootable','on']
        sortcmds.append('cmd05')

    if(args.vdi): # Existing VDI
        vdi_name=args.vdi
        cmds["cmd07"]=['vboxmanage','storageattach',args.name,'--storagectl','sata0','--device','0','--port','0','--type','hdd','--medium',vdi_name]
        sortcmds.append('cmd07')
    elif(args.hdd): # New VDI
        if(args.vdis):
            vdi_name="%s/%s.vdi" % (args.vdis,args.name)
        else:
            vdi_name="%s.vdi" % (args.name)
        cmds["cmd06"]=['vboxmanage','createhd','--filename',vdi_name,'--size',str(args.hdd)]
        cmds["cmd07"]=['vboxmanage','storageattach',args.name,'--storagectl','sata0','--device','0','--port','0','--type','hdd','--medium',vdi_name]
        sortcmds.append('cmd06')
        sortcmds.append('cmd07')
    else: # Error missing data
        print_error("Missing HDD size or VDI file")

    if(args.iso):
        cmds["cmd08"]=['vboxmanage','storageattach',args.name,'--storagectl','ide0','--port','0','--device','1','--type','dvddrive','--medium',args.iso]
        sortcmds.append('cmd08')

    if(args.hi):
        cmds["cmd09"]=['vboxmanage','modifyvm',args.name,'--nic2','hostonly','--hostonlyadapter2',args.hi]
        sortcmds.append('cmd09')

    if(args.vrde):
        sortcmds.append('cmd10')
        if(args.vp):
            cmds["cmd10"]=['vboxmanage','modifyvm',args.name,'--vrde','on','--vrdeport',str(args.vp)]
        else:
            cmds["cmd10"]=['vboxmanage','modifyvm',args.name,'--vrde','on']

    if(args.vp):
        cmds["cmd11"]=['vboxmanage','modifyvm',args.name,'--vrde','on']
        sortcmds.append('cmd11')

    print("===> Starting Creation<===")
    for cmd in sortcmds:
        print_pass(cmd,cmds[cmd])
        res=subprocess.call(cmds[cmd])
        if(not res == 0):
            print_error("Failed pass: %s" % (cmd))

parser = argparse.ArgumentParser(description='=> VirtualBox VM Creator <=',epilog='Ex/Ej: python createvm.py myvm Ubuntu_64 1024 -cpus 2 -hds 8192 -vdis $HOME/vdis -hi vboxnet0 -iso $HOME/ubuntu.iso')

grp1=parser.add_argument_group('Required/Requerido')
grp1.add_argument('name', action="store", help="VM Name/Nombre")
grp1.add_argument('ostype', action="store", help="VM's OS Type / Tipo de sistema operativo (list/lista: vboxmanage list ostypes)")
grp1.add_argument('ram', action="store",  type=int, help="VM's RAM (MBs)/Cantidad de RAM")

grp2=parser.add_argument_group('Others/Otros')
grp2.add_argument('-cpus', '--cpus', action="store", dest="cpu",type=int, help="VM's Cores / Cantidad núcleos")
grp2.add_argument('-hi', '--hostonly-if', action="store", dest="hi", help="HostOnly IF's name / Nombre interface HostOnly. (list/lista:  vboxmanage list hostonlyifs")
grp2.add_argument('-sata', '--sata', action="store_true", default=True, dest="sata", help="Create SATA bus / Crear bus SATA. Default: True")
grp2.add_argument('-ide', '--ide', action="store_true", default=True, dest="ide", help="Create IDE bus / Crear bus IDE. Default: True")

grp3=parser.add_argument_group('Remote Access/Acceso Remoto')
grp3.add_argument('-vrde', '--enable-vrde', action="store_true", default=True, dest="vrde", help="Allow remote desktop to this VM / Permitir escritorio remoto a esta VM. Default: True")
grp3.add_argument('-vp', '--vrde-port', action="store", default='3389', type=int, dest="vp", help="VRDE Port for this VM / Puerto para VRDE a esta VM. Default: 3389")

grp4=parser.add_argument_group('Extra files/ Archivos extra')
grp4.add_argument('-iso', '-iso-file', action="store", dest="iso", help="ISO image file / Imagen ISO")
grp4.add_argument('-vdis', '--vdi-folder', action="store", dest="vdis", help="VDI's storage path/ Ruta almacenamiento VDIs")
grp4.add_argument('-hds', '--hdd-size', action="store", dest="hdd",type=int, help="VM's HDD size (MBs)/ Espacio en Disco")
grp4.add_argument('-vdi', '--hdd-vdi', action="store", dest="vdi",help="VM VDI file (If not defined, will be created with same name than VM) / Archivo VDI (Si no se especifica, se creará uno con el mismo nombre de la VM.")

result=parser.parse_args()
createVM(result)
