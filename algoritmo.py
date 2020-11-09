# -*- coding: utf-8 -*-
import math

#Funcion:desest, calcula la disviación estandat de un conjunto de valores
#INPUT: arreglo de flotantes
#OUTPUT: flotante
def desest(vcdda):
    lista2  =  []
    A  =  len(vcdda)
    suma = 0
    varis = 0
    if A>1:
        for i in vcdda:
            suma +=  i
        p  =  ((suma+0.0)/(A+0.0))
        for j in range((A)):
            sumat  =  (vcdda[j]-p)**2
            lista2.append(sumat)
        for k in lista2:
            varis +=  k
        vari  =  varis
        va  =  math.sqrt((vari+0.0)/(A+0.0))
        return(va)

#Funcion: costo, calcula el
#INPUT:
#OUTPUT:

def costo(carga,espacio,hops):
    print 'carga',carga
    tau = 21
    gamma = 1000
    v1 = math.pow(math.pow(abs(gamma-carga)*10, -3),2)
    v2 = math.pow(math.pow(abs(tau-espacio)*10, -6),2)
    a = []
    b = []
    a = [math.pow(gamma*10,-3), math.pow(carga*10, -3)]

    b = [math.pow(tau*10,-6), math.pow(espacio*10, -6)]

    des1 = desest(a)
    des2 = desest(b)
    cost = math.exp(-((v1/des1)+(v2/des2)+(hops**2/hops**2)))
    return cost


#Funcion:
#INPUT:
#OUTPUT:

def calcula(vecinos):
    entrada = []
    distancia = []
    factor = []
    producto = []
    peso = []
    consenso = []
    q = 2
    tam_d = 0

    
    print 'llegan estos vecinos',len(vecinos)

    for i in range(len(vecinos)):
            carga= vecinos[i].carga;
            espacio=vecinos[i].espacio;
            print espacio
            print 'prueba carga',float(carga)
            y = costo(float(carga),float(espacio),1)
            entrada.append(y)
            print 'y',y

    for k in range (len(entrada)-1):
        j = k+1
        for j in range(len(entrada)):
            d = abs(entrada[k]-entrada[k+1])
            distancia.append(d)
            fac = 1/(1+math.pow((d/0.5), q))
            factor.append(fac)
        tam_d = len(distancia)
    print tam_d
    for m in range (len(entrada)):
        p = 1
        for j in range(tam_d):
            p = p*factor[j]
        w = 1/(1+p)
        con = w*float(entrada[m])
        producto.append(p)
        peso.append(w)
        consenso.append(con)
    weight = sum(peso)
    y = sum(consenso)/weight

    aprox = []
    for h in range(len(entrada)):
        ap = abs(y-entrada[h])
        aprox.append(ap)
    temp = min(aprox)
    for g in range(len(entrada)):
        if temp == aprox[g]:
            ganador = g
            break
    return ganador    
    #q.put(ganador)
