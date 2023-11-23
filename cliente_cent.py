from __future__ import print_function
import os
import sys

import grpc

import pares_pb2
import pares_pb2_grpc


if __name__ == '__main__':
    servidorID = sys.argv[1]
    channel = grpc.insecure_channel(servidorID)
    stub = pares_pb2_grpc.ServidorCentralStub(channel)
    try:
        while True:
            procedimento = input().strip()
            if procedimento.startswith('T'):
                response = stub.Terminacao(pares_pb2.reqT())
                print(response.retorno)
                break
            elif procedimento.startswith('C,'):
                _, chave = procedimento.split(',', 1)
                id_servico = stub.Mapa(pares_pb2.reqC(chave=int(chave))).id
                if id_servico == None:
                    continue
                channel = grpc.insecure_channel(id_servico)
                stub = pares_pb2_grpc.ServidorParesStub(channel)
                response = stub.Consulta(pares_pb2.reqC(chave=int(chave)))
                
                print(f"{id_servico}: {response.valor}", end="")
            
    except  EOFError:
        channel.close()
        sys.exit(0)
