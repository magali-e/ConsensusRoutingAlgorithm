# -*- coding: utf-8 -*-
import sys
import threading
from multiprocessing import Queue
from comunicacion import activo
from comunicacion import envia_info
from comunicacion import busca
from comunicacion import activa_nodo


#sys.argv
ids={"andromeda":0,"cygnus":1,"auriga":2,"lebreles":3,"camelopardis":4,
"casiopea":5,"cetus":6,"chamaeleon":7,"columba":8,"crux":9,"draco":10,
"hydra":11,"lepus":12,"lyra":13,"phoenix":14,"prueba":15}

puerto=5555


def fuente(flag,id1,obj,q, ban):
    print 'id1 general',id1
   
    listo=busca(id1,obj)
    print listo
    if listo==2:
        print "El objetivo esta en el vecindario \n"
    else:
        hilo1 =threading.Thread(target=activo, args=(flag,id1,obj,q))
        hilo2 =threading.Thread(target=envia_info, args=(flag,id1))    
        hilo1.start()
        hilo2.start()
        x=q.get()
        print 'valor devuelto por la fuente ', x
        if x!=id1:
            ban.put(0)
        else: 
            ban.put(1)
        
        
def nodo(flag,id1,obj,q,ban):
    print id1
    if ban.empty()==True:
        hilo2 =threading.Thread(target=envia_info, args=(flag,id1))
        hilo2.start()
        hilo2.join()
    else:
        ban.put(1)      

def segundo(flag,id1,obj,q):
    #obj=q1.get()
    flag=activa_nodo(id1,obj)
    ban.put(flag)



def terminar(flag,id1,obj,q,ban):
    print "el objetivo ha sido alcanzado"
    ban.put(1)

#nodo que inicia

#if (len(sys.argv)!=4):
#    print "error de parametros"
#    print "uso: para fuente",sys.argv[0], "nombre del programa nombre del dispositivo objetivo bandera"
#    print "uso: para nodo",sys.argv[0], "nombre del programa nombre del dispositivo bandera"
#    sys.exit(-1)

if (len(sys.argv)==4):
    name=sys.argv[1]
    objetivo=sys.argv[2]
    flag=sys.argv[3]
    id1=ids[name]
    obj=ids[objetivo]
else:
    name=sys.argv[1]
    flag=sys.argv[2]  
    id1=ids[name] 
    obj=0;

operaciones = { '0': nodo,'1': fuente,  '2': segundo,'3':terminar}
 


if __name__ == "__main__":
    f=int(flag)
    ban=Queue()
    q=Queue()
    #q1=Queue()
    print 'id, flag',id1,flag
    #q1.put(obj)
    #while isinstance(flag,int)==True:
    while 1:
        operaciones[str(f)](flag,id1,obj,q, ban)
        flag=ban.get()
        f=int(flag)
        print "BANDERA",flag
        
        

            
    
    
