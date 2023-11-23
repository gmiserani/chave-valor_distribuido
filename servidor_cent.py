import grpc
from concurrent import futures
import threading
import pares_pb2
import pares_pb2_grpc
import sys

class ServidorCentral(pares_pb2_grpc.ServidorCentralServicer):
    def __init__(self, stop_event):
        self.chaves = {}
        self.stop_event = stop_event

    def Registro(self, request, context):
        for chave in request.chaves:
            self.chaves[chave] = request.id
        return pares_pb2.registro(cont=len(request.chaves))
    
    def Mapa(self, request, context):
        for chave in self.chaves:
            if chave == request.chave:
                return pares_pb2.mapa(id=self.chaves[chave])
        return pares_pb2.mapa(id=None)

    def Terminacao(self, request, context):
        self.stop_event.set()
        return pares_pb2.termino(retorno=len(self.chaves))


def serve(port):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pares_pb2_grpc.add_ServidorCentralServicer_to_server(ServidorCentral(stop_event), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    stop_event.wait()
    server.stop(0)

if __name__ == '__main__':
    port = sys.argv[1]

    serve(port)