
'''import flask.views
from flask import make_response
#from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from models.bdCreator import Session'''

#sesion=Session()

class Nodo:
    cicloImprimir=dict()
    def __init__(self, idItem, nombre, idFase):
        self.idItem=idItem;
        self.idFase=idFase;
        self.nombre=nombre;
        self.lista=[];
        
        
    def agregarRelacion(self,nodo):
        if nodo is not None and self.lista.count(nodo)==0 and nodo.idItem!=self.idItem:
            self.lista.append(nodo);
            return 1;
        else:
            return 0;
    def eliminarRelacion(self,nodo):
        if nodo is not None and self.lista.count(nodo)==1:
            self.lista.remove(nodo);
            return 1;
        else:
            return 0;
    def tieneRelacionCon(self,nodo):
        if nodo is not None and self.lista.count(nodo)==1:
            return 1;
        else:
            return 0;

   
    def probarSiTieneCiclo(self, nodo):
        r=0;  
        aux=0;    
        if self.idFase==nodo.idFase:                
            #print("ahora estoy en "+str(self.idItem))
            for n in self.lista:
                #print("me voy al padre  "+str(n.idItem))
                if n.idItem==nodo.idItem:
                    r=1; #hay ciclo
                    print(self.idItem)
                    self.cicloImprimir[self.idItem]=self.nombre;
                else:
                    r=n.probarSiTieneCiclo(nodo);
                    if(r==1):
                        print(self.idItem)
                        self.cicloImprimir[self.idItem]=self.nombre;
                        break;
                    
                    
            return r;
    def imprimirList(self):
        for i in list:
            print(str(i)+'->')
    def imprimirHijo(self, cad):
        print("Hijo de"+cad)
        for i in self.lista:
            print (i.idItem)
    
    def esIgualA(self, nodo):
        if(self.idItem==nodo.idItem and self.idFase==nodo.idFase):
            return 1;
        else:
            return 0;
'''n1=Nodo(1,"nodo1",1)
n2=Nodo(2,"nodo2",1)
n3=Nodo(3,"nodo3",1)
n4=Nodo(4,"nodo4",1)
n5=Nodo(5,"nodo5",1)
n6=Nodo(6,"nodo6",1)
n7=Nodo(7,"nodo7",1)

n1.agregarRelacion(n2)
n1.agregarRelacion(n3)
#n1.agregarRelacion(n4)

n2.agregarRelacion(n4)
n3.agregarRelacion(n2)
n4.agregarRelacion(n1)

n1.imprimirHijo("n1")
n2.imprimirHijo("n2")
n3.imprimirHijo("n3")
n4.imprimirHijo("n4")


print("el ciclo es")
#print("tiene ciclo?"+str(n1.probarSiTieneCiclo(n1)))

#Nodo.imprimirList()

'''