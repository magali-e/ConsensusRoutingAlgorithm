#! /usr/bin/env python
# -*- coding: utf8 -*-

import socket
import SocketServer
import threading
import sys
import logging

#Configura el log
logging.basicConfig(level=logging.DEBUG,format="%(name)s: %(message)s")

#Tamaño de los buffers de envío/recepcion
IP_PRUEBA='192.168.10.111'
BUFFER_SIZE=1024

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger=logging.getLogger('RequestHandler')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        self.logger.debug('Iniciando Handler')
        return

    def setup(self):
        return SocketServer.BaseRequestHandler.setup(self)

    def finish(self):
        return SocketServer.BaseRequestHandler.finish(self)

    def handle(self):
        self.logger.debug('Recibiendo...')
        obj = self.request.recv(BUFFER_SIZE)
        self.logger.debug(obj)
        response = "hola desde aqui"
        assert sys.getsizeof(response)<=BUFFER_SIZE
        self.request.send(response)

class EchoServer(SocketServer.TCPServer):
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger=logging.getLogger('EchoServer')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug("Iniciando el servidor")
        while True:
            self.handle_request()
        return

    def handle_request(self):
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        return SocketServer.TCPServer.close_request(self, request_address)

class Nodo:
    def __init__(self):
        self.logger=logging.getLogger('Nodo creado')
        
        
    def sirvete(self,ip=IP_PRUEBA,puerto=5555):
        self.logger=logging.getLogger('Nodo(%s)'%ip)
        self.ip=ip
        self.puerto=puerto
        self.logger.debug("Iniciando servidor")
        self.servidor=EchoServer((ip,puerto),EchoRequestHandler)
        self.threadServidor=threading.Thread(target=self.servidor.serve_forever)
        self.threadServidor.start()
        self.logger.debug("Iniciado")
    def comunicate(self,ip=IP_PRUEBA,puerto=5556):
        self.logger.debug('Iniciando comunicacion')
        mensaje="Te envio un mensaje"
        assert sys.getsizeof(mensaje) <= BUFFER_SIZE
        com_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.logger.debug('Iniciando conexion')
        com_socket.connect((ip,puerto))   
        self.logger.debug('Enviando mensaje')
        bytes_enviados=com_socket.send(mensaje)
        self.logger.debug('Enviados %d bytes'%bytes_enviados)
        self.logger.debug('Recibiendo respuesta')
        respuesta=com_socket.recv(BUFFER_SIZE)
        self.logger.debug('Cerrando socket')
        com_socket.close()
        self.logger.debug("Recibí: "+respuesta)
        return respuesta

  

##miNodo1=Nodo(puerto=5555)
##miNodo2=Nodo(puerto=5555)
##
##thread1=threading.Thread(target=miNodo1.comunicate,args=(IP_PRUEBA,5555))
##thread1.start()
##thread2=threading.Thread(target=miNodo1.comunicate,args=(IP_PRUEBA,5555))
##thread2.start()
##thread3=threading.Thread(target=miNodo2.comunicate,args=(IP_PRUEBA,5555))
##thread3.start()
##thread4=threading.Thread(target=miNodo2.comunicate,args=(IP_PRUEBA,5560))
##thread4.start()
