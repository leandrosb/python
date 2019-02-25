# -*- coding: utf-8 -*-
from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from subprocess import call

import sys
import csv
import atexit
import ssl
import time
import getpass
import argparse

def conecta(vcenter, login, senha):
    try:
       context = None
       if hasattr(ssl, '_create_unverified_context'):
          context = ssl._create_unverified_context()
       conn = SmartConnect(host=vcenter, user=login, pwd=senha, port=443, sslContext=context)
       atexit.register(Disconnect, conn)
       return conn.RetrieveContent()
    except vmodl.MethodFault as e:
      print("Falha vmodl: %s" % e.msg)
      return 1
    except Exception as  e:
      print("Falha excecao: %s" % str(e))
      return 1

def get_args():
    parser = argparse.ArgumentParser(prog='resizing',
        description='Argumentos para alterar o flavor no Vcenter')

    parser.add_argument('--arquivo','-a',
                        required=True,
                        action='store',
                        default=None,
                        help='Informe o arquivo a ser utilizado')
    parser.add_argument('--workes','-w',
                        required=False,
                        action='store',
                        default=None,
                        help='Informe a quantidade de workes')
    args = parser.parse_args()
    return args

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

def ler_arquivo( arquivo):
    lista = []
    with open(arquivo,"r",newline='') as file_csv:
         linha_csv = csv.reader(file_csv, delimiter=';', quoting=csv.QUOTE_ALL)
         for linha in linha_csv:
             lista.append(linha)
         file_csv.close()
    return lista


def main():
    args = get_args()
    lista_arquivo = ler_arquivo(args.arquivo)
    num_workers = args.workes





if __name__ == "__main__":
    main()
