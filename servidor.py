from concurrent import futures

import grpc
import socket

import sys
import threading
import pares_pb2
import pares_pb2_grpc

class Pares(pares_pb2_grpc.ServidorParesServicer):
    def __init__(self, stop_event):
        self.pares = {}
        self.stop_event = stop_event

    def Inserir(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.insercao(retorno=-1)
        else:
            self.pares[request.chave] = request.valor
            return pares_pb2.insercao(retorno=0)
    
    def Consulta(self, request, context):
        if request.chave in self.pares:
            return pares_pb2.consulta(valor=self.pares[request.chave])
        else:
            return pares_pb2.consulta(valor=None)
        
    def Ativacao(self, request, context):
        if (len(sys.argv)==3):
            channel = grpc.insecure_channel(request.id)
            stub = pares_pb2_grpc.ServidorCentralStub(channel)
            response = stub.Registro(pares_pb2.reqR(id_servico=f"{socket.getfqdn()}:{sys.argv[1]}", chaves=self.pares.keys()))
            
            return pares_pb2.ativacao(cont=response.cont)
        else:
            return pares_pb2.ativacao(cont=0)
            

    def Terminacao(self, request, context):
        self.stop_event.set()
        return pares_pb2.termino(retorno=0)

def serve(port):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pares_pb2_grpc.add_ServidorParesServicer_to_server(Pares(stop_event), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    stop_event.wait()
    server.stop(0)

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        port = sys.argv[1]

    if (len(sys.argv) == 3):
        port = sys.argv[1]
        flag = sys.argv[2]

    serve(port)
        