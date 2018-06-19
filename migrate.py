#!/usr/bin/env python


import atexit
import argparse
import sys
import time
import ssl

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect


def get_objeto(content, vimtype, name):
    """
    Assossiando nome ao objeto
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
           obj = c
           break
    return obj


def wait_task(task, actionName='job', hideResult=False):

    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("tem error na Task")
            task_done = True

def main():

    if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()


    try:
       si = None
       try:
          si = connect.Connect(host="lxl1vmwvc001", user="administrator@vsphere.lab", pwd="vmw@r3Esx1", port=443, sslContext=context)
       except IOError as e:
          pass
          atexit,register(Disconnect, si)


       content = si.RetrieveContent()

       datacenter = get_objeto(content, [vim.Datacenter],'CCTI')

       vmFolder = datacenter.vmFolder
       vm = get_objeto(content, [vim.VirtualMachine], 'tf-leandro001')
       destination_host = get_objeto(content, [vim.HostSystem], 'xvd042.df.intrabb.bb.com.br')


       destination_storage = get_objeto(content, [vim.Datastore],'VMW_LAB_VSPHERE_dvol1')

       resource_pool = get_objeto(content, [vim.ResourcePool], 'LAB')

       if vm.runtime.powerState == 'powerOff':
          print('Alerta! Migracao apenas para vm power OFF')
          sys.exit()

       migrate_priority = vim.VirtualMachine.MovePriority.defaultPriority

       msg = " Migrando tf-leandro001 para DataStore %s " % (destination_storage)
       print(msg)


       """
       A magia começa aqui
       """
       vm_relocate_spec = vim.vm.RelocateSpec()
       vm_relocate_spec.host = destination_host
       vm_relocate_spec.pool = resource_pool

       #vm_relocate_spec.folder = vmFolder
       vm_relocate_spec.datastore = destination_storage


       task = vm.Relocate(spec=vm_relocate_spec)

       """
       esperando terminar a migracao
       """
       wait_task(task)

    except vmodl.MethodFault as e:
       print("Falha vmodl: %s" % e.msg)
       return 1
    except Exception as  e:
       print("Falha excecao: %s" % str(e))
       return 1


#star program
if __name__ == "__main__":
   main()

