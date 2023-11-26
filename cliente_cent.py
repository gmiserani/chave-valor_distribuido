from __future__ import print_function
import os
import sys

import grpc

import pares_pb2
import pares_pb2_grpc


if __name__ == '__main__':
    #pega a porta da linha de entrada
    servidorID = sys.argv[1]
    #inicializa canal com o servidor_cent
    channel = grpc.insecure_channel(servidorID)
    #cria um stub para chamadas rpc com o servidor
    stub = pares_pb2_grpc.ServidorCentralStub(channel)
    try:
        #le da entrada enquando não houver um exit
        while True:
            procedimento = input().strip()
            #verifica se o valor de entrada é o referente ao da terminacao da conexao
            if procedimento.startswith('T'):
                #chama a resposta de terminacao do request feito ao servidor
                response = stub.Terminacao(pares_pb2.reqT())
                #imprime o número de chaves que estavam registradas
                print(response.retorno)
                break
            #verifica se o valor de entrada é o referente ao da consulta
            elif procedimento.startswith('C,'):
                _, chave = procedimento.split(',', 1)
                channel = grpc.insecure_channel(servidorID)
                stub = pares_pb2_grpc.ServidorCentralStub(channel)
                #mapeia o servidor em busca da chave e pega o valor correspondente
                id_servico = stub.Mapa(pares_pb2.reqC(chave=int(chave)))
                if id_servico.id_servico == "":
                    continue
                channel = grpc.insecure_channel(id_servico.id_servico)
                stub = pares_pb2_grpc.ServidorParesStub(channel)
                response = stub.Consulta(pares_pb2.reqC(chave=int(chave)))
                
                print(f"{id_servico.id_servico}: {response.valor}")
            
    except  EOFError:
        channel.close()
        sys.exit(0)
