from concurrent import futures

import grpc
import sys

import pares_pb2
import pares_pb2_grpc

class Pares(pares_pb2_grpc.ParesServicer):
    def __init__(self, server):
        self.pares = {}
        self.server = server

    def Inserir(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.insercao(retorno=-1)
        else:
            self.pares[request.chave] = request.valor
            return pares_pb2.insercao(retorno=0)
    
    def Consultar(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.consulta(valor=self.pares[request.chave])
        else:
            return pares_pb2.consulta(valor=None)
        
    def Ativacao(self, request, context):
        
        if request.ativacao == True:
            self.server.stop(0)
            return pares_pb2.AtivacaoReply(mensaje="Servidor desactivado")
        else:
            return pares_pb2.AtivacaoReply(mensaje="Servidor activado")
    def Terminacao(self, request, context):
        return pares_pb2.termino(mensaje="Servidor terminado")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pares_pb2_grpc.add_ParesServicer_to_server(Pares(), server)
    server.add_insecure_port('[::]:' + portnumber)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    port = sys.argv[1]
    if len(sys.argv) == 3:
        