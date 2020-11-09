
# -*- coding: utf-8 -*-
import socket
import SocketServer
import os
import logging
import threading
import sys
import logging
import time

from algoritmo import calcula
from vecinos import Vecino
from multiprocessing import Queue
#arreglo con las direcciones ips de los dispositivos

ids_names = {"andromeda":0, "cygnus":1, "auriga":2, "lebreles":3, "camelopardis":4,
"casiopea":5, "cetus":6, "chamaeleon":7, "columba":8, "crux":9, "draco":10,
"hydra":11, "lepus":12, "lyra":13, "phoenix":14, "prueba":15, "omicronpersei8":16}

ids_num = {"192.168.10.109":0, "192.168.10.115":1, "192.168.10.113":2,
"192.168.10.110":3, "192.168.10.111":4, "192.168.10.112":5, "192.168.10.108":6,
"192.168.10.116":7, "192.168.10.105":8, "192.168.10.103":9, "192.168.10.104":10,
"192.168.10.106":11, "192.168.10.136":12, "192.168.10.107":13, "192.168.10.142":14,
"132.248.51.123":15, "127.0.1.1":16}


ids = ['192.168.10.109', '192.168.10.115', '192.168.10.113', '192.168.10.110',
'192.168.10.111', '192.168.10.112', '192.168.10.108','192.168.10.116',
'192.168.10.105', '192.168.10.103', '192.168.10.104','192.168.10.106',
'192.168.10.136', '192.168.10.107', '192.168.10.142','132.248.51.123', '127.0.1.1']

#lista de listas de los vecindarios de cada nodo

vecindarios = [
['192.168.10.108', '192.168.10.115', '192.168.10.113', '192.168.10.110'],
['192.168.10.104', '192.168.10.106', '192.168.10.113', '192.168.10.109'],
['192.168.10.106', '192.168.10.115', '192.168.10.109', '192.168.10.116', '192.168.10.108'],
['192.168.10.109', '192.168.10.108', '192.168.10.111'],
['192.168.10.110', '192.168.10.108', '192.168.10.105', '192.168.10.112'],
['192.168.10.111', '192.168.10.105', '192.168.10.103'],
['192.168.10.109', '192.168.10.110', '192.168.10.113', '192.168.10.116', '192.168.10.105', '192.168.10.111'],
['192.168.10.113', '192.168.10.108', '192.168.10.105', '192.168.10.107', '192.168.10.142'],
['192.168.10.116', '192.168.10.111', '192.168.10.105', '192.168.10.108', '192.168.10.112', '192.168.10.103', '192.168.10.107'],
['192.168.10.105', '192.168.10.112', '192.168.10.107', '192.168.10.136'],
['192.168.10.106', '192.168.10.115'],
['192.168.10.115', '192.168.10.113', '192.168.10.104'],
['192.168.10.142', '192.168.10.107', '192.168.10.103'],
['192.168.10.105', '192.168.10.116', '192.168.10.142', '192.168.10.103', '192.168.10.136'],
['192.168.10.107', '192.168.10.116', '192.168.10.136'],
['132.248.51.123'], ['127.0.1.1']]


#Configura el log
logging.basicConfig(level=logging.DEBUG,format="%(name)s: %(message)s")

#Tamaño de los buffers de envío/recepcion
#IP_PRUEBA='192.168.10.113'
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
        name = socket.gethostname()
        print "handle", name
        id_local = ids_names[name.lower()]
        ip_local = ids[id_local]        
        print "carga", get_carga(ip_local)
        data1 = str(get_carga(ip_local))+',' +str(get_espacio())+','+str(0)
        self.logger.debug('Recibiendo...')
        obj = self.request.recv(BUFFER_SIZE)
        self.logger.debug(obj)
        response = data1
        assert sys.getsizeof(response)<=BUFFER_SIZE
        self.request.send(response)
        activa_nodo(ip_local, obj)

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
        
        
    def sirvete(self,ip,puerto):
        self.logger=logging.getLogger('Nodo(%s)'%ip)
        self.ip=ip
        self.puerto=puerto
        self.logger.debug("Iniciando servidor")
        self.servidor=EchoServer((ip,puerto),EchoRequestHandler)
        self.threadServidor=threading.Thread(target=self.servidor.serve_forever)
        self.threadServidor.start()
        self.logger.debug("Iniciado")
        
    def comunicate(self,ip,puerto,obj):
        self.logger.debug('Iniciando comunicacion')
        mensaje=str(obj)
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
      

"""
#Funcion que busca el nodo objetivo en un vecindario dado,
#INPUT:  id del nodo y  la direccion IP del nodo objetivo
#OUTPUT: 2 si es encontrado, 0 si no
"""
def busca(id1, obj):
    import time
    tmp1=time.clock()
    j=1
    print 'buscando', id1, obj, ids[obj]
    h = len(vecindarios[id1])
    print "longitud vecindario", h
    dos = ids[obj]
    d = dos.split(".")
    for i in range(h):
        uno = vecindarios[id1][i]
        e = uno.split(".")
        print d[3], e[3]
        if int(d[3])==int(e[3]):
            j = 2
            break
        else:
            j = 0
    print "j enviada al nodo ", j
    tmp2=time.clock()
    print "delay de busqueda",tmp2-tmp1
    return j

#Funcion se conecta a una ip y recibe información
#INPUT: id local e id remoto
#OUTPUT: un paquete de datos correspondiente a carga y espacio de un vecino dado


def recibe_info(id1, id2, obj):
    miNode=Nodo()
    respuesta= miNode.comunicate(ip=id2,puerto=5555, obj=obj)
    #print 'datos antes de los puntos',data
    datos= respuesta.split(',')
    print 'recibe datos',datos
    if len(datos) == 3:
        vecino = id2
        carga = datos[0]
        espacio = datos[1]
        print "rastro 1", datos
        #print 'lo que se va', id2,datos[0],datos[1]
    return(vecino,carga,espacio)



#funcion envia_info: abre conexión de un socket y envia la información de su estado
#INPUT:  id local, id remota
#OUTPUT: null

def envia_info(flag,id1):
    miNodo1=Nodo()
    miNodo1.sirvete(ip=ids[id1],puerto=5555)
    
#Funcion solicita: solicita informacion a un nodo remoto
#INPUT:  id local, id remota
#OUTPUT:   tupla con la información de estado de id2

def solicita(id1, id2, obj):
    print id2, id1
    print "id1", id1
    info=recibe_info(id1, id2, obj)
    print "informacion recibida", info
    return info


#Funcion carga: obtiene la información de carga en el canal de un nodo dado
#INPUT: IP
#OUTPUT: valor flotante
def get_carga(ip):
    print ip
    p = os.popen("ping -c 1 %s| head -2 | tail -1 | cut -f4 -d'=' | cut -f1 -d' '" % ip,'r')
    line = p.readline()
    if not line:
        return 0
    else :
        load = line
        j_carga = float(load.split('\n')[0])
        return j_carga



#Funcion espacio: obtiene la información de espacio en el planificador de tareas
#INPUT:
#OUTPUT:   valor flotante correspondiente al espacio

def get_espacio():

    p = os.popen("mpstat | tail -1 | cut -f 41-44 -d' '",'r')
    line = p.readline()
    if not line:
        return 0
    else:
        space = line
        print 'space', line
        #h=space.split(':')[0]
        j = float(space.split('O\n')[0])
        #print 'los 2 puntos', j
        return j

def activa_nodo(id1, obj):
    #import time
    t1=time.clock()
    print "objetivo activo", obj
    obje = int(obj)
    q1 = Queue()
    v = len(vecindarios[ids_num[id1]])
    for i in range(v):
        idlocal=ids_num[id1]
        mask= ids_num[vecindarios[idlocal][i]]
        j = busca(mask,obje)
        print j
        if j == 2:
            ganador = vecindarios[idlocal][i]
            q1.put(ganador)
            break
    t2=time.clock()
    print "delay activa_nodo", str(float(t2-t1))

    activo(1,ids_num[id1], obje, q1)

#Funcion correspondiente al estado de busqueda de un nodo objetivo
#INPUT:  flag y su id
#OUTPUT:   flag

def activo(flag, id1, obj, q):
    t1=time.clock()
    if q.empty==False:
        ganador=q.get()
        print 'ip', ganador
        q.put(ganador)
        flag=3
    else: 
        if int(flag) == 1:
            v=len(vecindarios[id1])
            vecinos = []
            f1, f2 = info_propia()
            a = Vecino(id1, f1, f2)
            print "rastro 0", a
            vecinos.append(a)
            for i in range(v):
                info = solicita(ids[id1], vecindarios[id1][i], obj)
                print "recibí la info del socket", info
                a = Vecino(info[0], info[1], info[2])
                vecinos.append(a)
                ganador = calcula(vecinos)
                print 'ganador', ganador
                print 'ip', vecindarios[id1][ganador]
                q.put(vecindarios[id1][ganador])
                if id1 == ganador:
                    flag = 3
                else:
                    flag = 2
    t2=time.clock()
    t=t1-t2
    print "delay funcion activo", str(float(t))
    return flag

        #print 'el ganador esta en la posicion %d con valores %d ' , ganador, vecindarios[id][ganador]


def info_propia():
    import time
    tm1=time.clock()
    name = socket.gethostname()
    print name
    id_local = ids_names[name.lower()]
    ip_local = ids[id_local]
    load = str(get_carga(ip_local))
    tim = str(get_espacio())
    print 'propia carga espacio', load, time
    tm2=time.clock()
    print "delay funcion info:propia", str(float(tm2-tm1))
    return load,tim