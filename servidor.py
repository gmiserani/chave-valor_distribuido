from concurrent import futures

import grpc
import socket

import sys
import threading
import pares_pb2
import pares_pb2_grpc

class Pares(pares_pb2_grpc.ServidorParesServicer):
    def __init__(self, stop_event, portNumber):
        self.pares = {}
        self.stop_event = stop_event
        self.portNumber = portNumber
# faz a insercao no dicionario o valor de descricao asssociado a uma chave
# retorna 0 caso a insercao seja feita e -1 caso ja haja esse valor
    def Inserir(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.insercao(retorno=-1)
        else:
            self.pares[request.chave] = request.valor
            return pares_pb2.insercao(retorno=0)
#procura o valor associado a uma chave recebida.
    def Consulta(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.consulta(valor=self.pares[request.chave])
        else:
            #da como resposta uma string nula caso nao exista a chave
            return pares_pb2.consulta(valor="")
#recebe o id de um servidor centralizador
    def Ativacao(self, request, context):
        if (len(sys.argv)==3):
            #conecta ao servidor centralizador
            channel = grpc.insecure_channel(request.id)
            stub = pares_pb2_grpc.ServidorCentralStub(channel)
            #faz o pedido de registro das chaves no servidor centralizador
            response = stub.Registro(pares_pb2.reqR(id_servico=f"{socket.getfqdn()}:{self.portNumber}", chaves=self.pares.keys()))
            #numero de chaves armazenadas
            return pares_pb2.cont(cont=response.cont)
        else:
            return pares_pb2.cont(cont=0)
            
#realiza a terminacao, dando a reposta 0 ao cliente
    def Terminacao(self, request, context):
        self.stop_event.set()
        return pares_pb2.termino(retorno=0)

def serve(port):
    #inicializacao do servidor e estabelecimento da conexão grpc
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pares_pb2_grpc.add_ServidorParesServicer_to_server(Pares(stop_event, sys.argv[1]), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    stop_event.wait()
    server.stop(0)

if __name__ == '__main__':
    #pega os valores de entrada
    if (len(sys.argv) == 2):
        port = sys.argv[1]

    if (len(sys.argv) == 3):
        port = sys.argv[1]
        flag = sys.argv[2]

    serve(port)
        