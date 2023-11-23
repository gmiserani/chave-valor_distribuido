from __future__ import print_function
import os
import sys

import grpc

import pares_pb2
import pares_pb2_grpc
def Inserir(stub, chave, valor):
    response = stub.Inserir(pares_pb2.reqI(chave=chave, valor=valor))
    print(response.retorno)

def Consultar(stub, chave):
    response = stub.Consulta(pares_pb2.reqC(chave=chave))
    print(response.valor)

def Ativacao(stub, id):
    response = stub.Ativacao(pares_pb2.reqA(id=id))
    print(response.cont)

def Terminacao(stub):
    response = stub.Terminacao(pares_pb2.reqT())
    print(response.retorno)

def run():
    servidorID = sys.argv[1]
    channel = grpc.insecure_channel(servidorID)
    stub = pares_pb2_grpc.ServidorParesStub(channel)
    try:
        while True:
            procedimento = input().strip()
            if procedimento.startswith('I,'):
                _, chave, valor = procedimento.split(',', 2)
                Inserir(stub, int(chave), valor)

            elif procedimento.startswith('C,'):
                _, chave = procedimento.split(',', 1)
                Consultar(stub, int(chave))

            elif procedimento.startswith('A,'):
                _, id = procedimento.split(',', 1)
                Ativacao(stub, id)
            
            elif procedimento.startswith('T'):
                Terminacao(stub)
                break

    except EOFError:
        channel.close()
        sys.exit(0)


if __name__ == '__main__':
    run()