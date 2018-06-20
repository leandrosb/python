#!/usr/bin/env python

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl

import atexit
import ssl
import humanize
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='Argumentos para migracao no Vcenter')


    parser.add_argument('--name','-n',
                        required=True,
                        action='store',
                        default=None,
                        help='Nome do datastore ou datastore-cluster de origem ')
    parser.add_argument('--destino','-d',
                        required=True,
                        action='store',
                        default=None,
                        help='Nome do datastore ou datastore-cluster de destino')
    args = parser.parse_args()
    return args


def wait_task(task, action='job', hideResult=False):
    task_done = False
    while not task_done:
       if task.info.state == 'success':
          return task.info.result

       if task.info.state == 'error':
          print("Tem erro na task")
          task_done = True


def get_obj(content, vimtype, name ):
    obj = None


    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
           if c.name == name:
              obj = c
              break
        else:
           obj = c
           break
    return obj

def Mostra_vm(vm):
    vmconfig = vm.summary
    print("Virtual Machine: ",vmconfig.config.name, "\nEstado: ", vmconfig.runtime.powerState,"\n")




def Mostra_datastore(datastore):
    try:
        summary = datastore.summary
        capacity = summary.capacity
        freeSpace = summary.freeSpace
        uncommittedSpace = summary.uncommitted
        freeSpacePercentage = (float(freeSpace) / capacity) * 100
        print("=================================================")
        print("Datastore name: ", summary.name)
        print("Capacidade: ", humanize.naturalsize(capacity, binary=True))
        utilizado = (capacity - freeSpace)
        print("Utilizado: ", humanize.naturalsize(utilizado, binary=True))
        if uncommittedSpace is not None:
            provisionedSpace = (capacity - freeSpace) + uncommittedSpace
            print("Provisionado: ", humanize.naturalsize(provisionedSpace,
                                                              binary=True))
        print("Espaco livre: ", humanize.naturalsize(freeSpace, binary=True))
        print("Percentual de espaco livre: " + str(freeSpacePercentage) + "%")
        print("Virtual Machines: ",format(len(datastore.vm)))
        vmList = datastore.vm
        for vm in vmList:
            Mostra_vm(vm)


        print("=================================================")
    except Exception as error:
        print("Unable to access summary for datastore: ", datastore.name)
        print(error)
        pass

def get_vm(vm):
    if vm is None:
       print("Virtual machine nao encontrada")
       exit(1)
    else:
       vm_details = vm.summary

    return vm_details.config.name

def main():

    args = get_args()

    context = None
    try:
       conn = None
       try:

          if hasattr(ssl, '_create_unverified_context'):
             context = ssl._create_unverified_context()

          conn = SmartConnect(host="lxl1vmwvc001", user="administrator@vsphere.lab", pwd="vmw@r3Esx1", port=443, sslContext=context)
       except IOError as e:
          pass
          atexit,register(Disconnect, conn)

       atexit.register(Disconnect, conn)
       content = conn.RetrieveContent()
       print("============DataStore de Origem==================")
       ori_datastore = get_obj(content,[vim.Datastore], args.name)
       Mostra_datastore(ori_datastore)

       print("============DataStore de Destino=================")
       dest_datastore = get_obj(content,[vim.Datastore], args.destino)
       Mostra_datastore(dest_datastore)

       for vmList in dest_datastore.vm:
           vm_name = get_vm(vmList)
           vm_migrate = get_obj(content,[vim.VirtualMachine], vm_name)
           migrate_priority = vim.VirtualMachine.MovePriority.defaultPriority
           vm_relocate_spec = vim.vm.RelocateSpec()
           vm_relocate_spec.datastore = dest_datastore
           task = vm_migrate.Relocate(spec=vm_relocate_spec)
           wait_task(task)

    except vmodl.MethodFault as e:
       print("Falha vmodl: %s" % e.msg)
       return 1
    except Exception as  e:
       print("Falha excecao: %s" % str(e))
       return 1





# Start program
if __name__ == "__main__":
   main()




