#!/usr/bin/env python


from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

import atexit
import ssl
import humanize


def get_obj (vim_type, name=None):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vim_type, True)
    if name:
        for c in container.view:
            if c.name == name:
                obj = c
                return [obj]
    else:
        return container.view



def PrintDataInfo(datastore):
    try:
        summary = datastore.summary
        capacity = summary.capacity
        freeSpace = summary.freeSpace
        uncommittedSpace = summary.uncommitted
        freeSpacePercentage = (float(freeSpace) / capacity) * 100
        print("=================================================")
        print("Datastore name: ", summary.name)
        print("Capacidade: ", humanize.naturalsize(capacity, binary=True))
        if uncommittedSpace is not None:
            provisionedSpace = (capacity - freeSpace) + uncommittedSpace
            print("Provisionado: ", humanize.naturalsize(provisionedSpace,
                                                              binary=True))
        print("Espaco livre: ", humanize.naturalsize(freeSpace, binary=True))
        print("Percentual de espaco livre: " + str(freeSpacePercentage) + "%")
        print("Virtual Machines: ",format(len(datastore.vm)))
        print("=================================================")
    except Exception as error:
        print("Unable to access summary for datastore: ", datastore.name)
        print(error)
        pass

def main():

   context = None
   if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()

   conn = SmartConnect(host="***", user="***********", pwd="*********", port=443, sslContext=context)

   atexit.register(Disconnect, conn)

   content = conn.RetrieveContent()
 for datacenter in content.rootFolder.childEntity:
      datastores = datacenter.datastore
      for ds in datastores:
          PrintDataInfo(ds)
   return 0

# Start program
if __name__ == "__main__":
   main()
