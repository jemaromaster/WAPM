from flask import views, make_response
import flask.views

from models.itemModelo import Item
from models.atributosModelo import Atributos
from models.bdCreator import Session
from models.historialModelo import HistorialRelacion

from models.faseModelo import Fase

from itemManejador import ItemManejador
from datetime import datetime
from Grafos.nodo import Nodo
from models.itemModelo import Item, Relacion

class ItemControllerClass(flask.views.MethodView):
            
    def controlarItem(self, f, idF, atributos, esReversion):
        f.nombreItem=f.nombreItem.strip()
        f.estado=f.estado.strip()
        f.descripcion=f.descripcion.strip()
        
        try:
            f.costo=int(f.costo)
            f.prioridad=int(f.prioridad)
            f.complejidad=int(f.complejidad)
            f.idFase=int(f.idFase)
            esReversion=int(esReversion)
        except:
            return make_response ('t, no se pudo castear a entero')
        
        '''controla el tamano de los strings'''
         
        if not(1<=len(f.nombreItem)<=20 \
              and 1<=len(f.descripcion)<=50 and 1<=len(f.estado)<=12 ): 
            return make_response('t,Se supera caracteres de los campos para el item')
            
        
        if not(isinstance(f.idFase, int)):
            return make_response('t,id Fase invalido no int ')
        
       
        '''consulta si es que existe ya item con ese nombre'''
        
        sesion=Session()
        
        qr=sesion.query(Item).filter(Item.idFase==f.idFase).filter(Item.nombreItem==f.nombreItem).first()
        
        '''se consulta primeramente si corresponde a un reversion'''
        if(esReversion==0): 
            if(idF==0):
                if(qr is not None):
                    sesion.close()
                    return make_response('t,Ya existe un item con el nombre indicado en la fase')
            else:
                if( qr is not None and str(qr.idItem) != idF ):
                    sesion.close()
                    return make_response('t,Ya existe un item con el nombre indicado en la fase')
        else: #es reversion
            if(qr is not None and str(qr.idItem) != idF):
                sesion.close()
                return make_response('t,Existe item que cuenta con el mismo nombre que la version a la cual desea\
                                            reversionar. Modifique el nombre del item "'+ qr.nombreItem + '" para poder reversionar' )
        
        
            q2=sesion.query(HistorialRelacion).filter(HistorialRelacion.hijo_id==f.idItem)\
                                             .filter(HistorialRelacion.versionHijo==esReversion)\
                                             .all()
            
            #########################################################33
            #se controla que no se este creando un ciclo a la hora de agregar las relaciones
            ##############################################################333
            q=sesion.query(Item).filter(Item.idFase==int(f.idFase)).filter(Item.estado=='activo').all()
        
            nLista=dict()
            #aca se crea el grafo
            p=None;
            h=None;
            for i in q:
                aux=Nodo(i.idItem, i.nombreItem,i.idFase);
                '''if(int(padre_id)==aux.idItem):
                    p=aux;
                elif(int(hijo_id)==aux.idItem):
                    h=aux;'''
                
                nLista[str(aux.idItem)]=aux #se utiliza un mapper
            
            #para cada nodo en estado activo y sea de la fase
            for i in nLista:
                #se obtiene los nodos padres
                q=sesion.query(Relacion).filter(Relacion.hijo_id==nLista[i].idItem).all();
                      
                #se crea la relacion con sus padres
                for s in q:
                    if(str(s.padre_id) in nLista):
                        nodo_rel=nLista[str(s.padre_id)];
                        nLista[i].agregarRelacion(nodo_rel)
            
            
            
            #para cada relacion de la version a reversionar se controla si no generara ciclo
            for hrel in q2:
                tienec=0;
                p=nLista[str(hrel.padre_id)]
                h=nLista[str(hrel.hijo_id)]
                if h is not None:
                    h.agregarRelacion(p);
                    print("el ciclo es")
                    tienec=h.probarSiTieneCiclo(h);
                    
                
                if(tienec==1):
                    cad=''
                    for a in Nodo.cicloImprimir:
                        cad=cad+'->'+Nodo.cicloImprimir[a];
                    cicloImprimir=dict()
                    
                    cad=cad[2:len(cad)]  
                    sesion.close()
                    return make_response('t,La version a la que desea reversion genera el siguiente ciclo: '\
                                         + cad +'. Se debe eliminar alguna relacion del grafo actual para poder reversionar a la version')
            
            ##########################################################################################
            ##########################################################################33
            ############################################################################
        
        if(esReversion==0):#cuando no es reversion
            if(idF==0):
                laFase=sesion.query(Fase).filter(Fase.idFase==f.idFase).first()
                f.tag=laFase.tag+ "."+ f.nombreItem
        #se valida la fecha 
       
        try:
            '''
            fi=datetime(int(f.fechaInicio[6:10]),\
                             int(f.fechaInicio[3:5]),\
                             int(f.fechaInicio[0:2]))
            ff=datetime(int(f.fechaFinalizacion[6:10]),\
                             int(f.fechaFinalizacion[3:5]),\
                             int(f.fechaFinalizacion[0:2]))
            '''
            fi=datetime(int(f.fechaInicio[6:10]),\
                             int(f.fechaInicio[0:2]),\
                             int(f.fechaInicio[3:5]))
            ff=datetime(int(f.fechaFinalizacion[6:10]),\
                             int(f.fechaFinalizacion[0:2]),\
                             int(f.fechaFinalizacion[3:5]))
            
        except:
            sesion.close()
            return make_response('t,Fecha invalida') 
        
        #se controla que fecha inicio sea menor que fecha finalizacion
        if not(fi<=ff):
            sesion.close()
            return make_response('t,Fecha finalizacion antes que fecha inicio')
        
        
        lista=[]
        sesion=Session()
        '''se controlan los atributos'''
       
        for at in atributos:
            a=sesion.query(Atributos)\
                                    .filter(Atributos.idAtributo==int(at['idAtributos'])).first()
            print "lalala"+str(at['idAtributos'])
            print a
            
            if (a is not None):
                if(a.tipoPrimarioId==1): #cadena
                    
                    if not(1<=len(at['valor'].strip())<=a.longitudCadena):
                        sesion.close() 
                        return make_response('t,Se supera caracteres de los campos del atributo '+ at['nombreAtributo'])
                    
                elif(a.tipoPrimarioId==2):#numerico
                    #controlar
                    2+2
                elif(a.tipoPrimarioId==3):
                    #controlar
                    2+2
                elif(a.tipoPrimarioId==4):
                    print(at["valor"])
                    at["valor"]=at["valor"][3:5]+"/"+at["valor"][0:2]+"/"+at["valor"][6:10]
                    print(at["valor"])
                    
                else:
                    sesion.close()
                    return make_response('t,Tipo primario invalido')
                
                lista.append(at)
            else:
                sesion.close()
                return make_response('t,No existe ese atributo')
        sesion.close()
      
        
        im=ItemManejador()
       
        return im.guardarItem(f, idF, lista, esReversion)
        