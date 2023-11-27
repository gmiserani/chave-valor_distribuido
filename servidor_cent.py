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
# pega o id do servico que corresponde a um servidor e a lista d chaves dele. 
    def Registro(self, request, context):
        id = request.id_servico
        for chave in request.chaves:
    #pega as chaves e armazena na lista associadas ao id.
            self.chaves[chave] = id
        return pares_pb2.cont(cont=len(request.chaves))
#pega o valor da chave e procura ela na lista
#retorna o id do servidor onde essa chave ta
    def Mapa(self, request, context):
        for chave in self.chaves:
            if chave == request.chave:
                return pares_pb2.mapa(id_servico=self.chaves[chave])
        return pares_pb2.mapa(id_servico="")
#encerra e retorna o numero de chaves armazenadas
    def Terminacao(self, request, context):
        self.stop_event.set()
        return pares_pb2.termino(retorno=len(self.chaves))


def serve(port):
    #faz a inicializacao do servidor e estabelece a conexao grpc
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pares_pb2_grpc.add_ServidorCentralServicer_to_server(ServidorCentral(stop_event), server)
    server.add_insecure_port('0.0.0.0:' + port)
    server.start()
    stop_event.wait()
    server.stop(0)

if __name__ == '__main__':
    #pega a porta
    port = sys.argv[1]

    serve(port)
