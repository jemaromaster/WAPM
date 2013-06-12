
import flask.views
from flask import make_response
from utils import login_required,controlRol
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from models.historialModelo import HistorialItem, HistorialRelacion
from models.bdCreator import Session
from models.instanciaAtributos import InstanciaNumerico, InstanciaCadena, InstanciaEntero, InstanciaFecha, InstanciaTipoItem

from Grafos.nodo import Nodo
sesion=Session()
class AgregarRelacion(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de \
    relacion al servidor. \Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo \
   
    """
    
    @login_required
    def post(self):
        """
        Metodo utilizado cuando se realiza una peticion de creacion de \
        relacion al servidor. 
        @type idPadre: String
        @param idPadre: id del item padre a relacionar
        @type idHijo: String
        @param idHijo: id del item hijo a relacionar
        @type version: String
        @param version: version del hijo a relacionar 
        """
        
        idFase=flask.request.form['id_Fase']
        padre_id=flask.request.form['padre_id']
        hijo_id=flask.request.form['hijo_id']
        version_hijo=flask.request.form['versionHijo']
        
        
        
        if controlRol(str(idFase),'item','administrar')==0:
            return "t, No posee permisos para realizar esta accion"
        
        
        #se realiza el control
        if(padre_id==hijo_id):
            sesion.close()
            return make_response('t,No se puede relacionar el item con el mismo item')
        
        q=sesion.query(Relacion).filter(Relacion.padre_id==padre_id).filter(Relacion.hijo_id==hijo_id).first();
        
        if(q is not None):
            sesion.close()
            return make_response('t,Ya existe esa relacion')
        
        q=sesion.query(Relacion).filter(Relacion.padre_id==hijo_id).filter(Relacion.hijo_id==padre_id).first();
        
        if(q is not None):
            sesion.close()
            return make_response('t,Ya existe la relacion inversa, genera una relacion circular')
        
        qp=sesion.query(Item).filter(Item.idItem==padre_id).first()
        qs=sesion.query(Item).filter(Item.idItem==hijo_id).first()
        
        if(qp is not None and qs is not None):
            if qp.idFase>qs.idFase:
                sesion.close()
                return make_response('t,No puede relacionar un item de una Fase posterior con una fase Anterior')
        
        
        if(qs.estado!="activo"):
            sesion.close()
            return make_response('t,Solamente puede relacionarse items con estado activo')
        
        q=sesion.query(Item).filter(Item.idFase==int(idFase)).filter(Item.estado=='activo').all()
        
        nLista=dict()
        #aca se crea el grafo
        p=None;
        h=None;
        for i in q:
            aux=Nodo(i.idItem, i.nombreItem,i.idFase);
            if(int(padre_id)==aux.idItem):
                p=aux;
            elif(int(hijo_id)==aux.idItem):
                h=aux;
            
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
        
        
        
        tienec=0;
        
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
            return make_response('t,La relacion que desea agregar genera el siguiente ciclo: '+ cad)
        
        #se ve el tema de la version con la relacion
        i=sesion.query(Item).filter(Item.idItem==hijo_id).first()
        if(i.version==int(version_hijo)-1): #hay que crear una nueva version del item porque es el primero a agregar en la version
            
            histoItem=HistorialItem(i.nombreItem, i.version, i.prioridad, i.costo, i.complejidad, i.fechaInicio, i.fechaFinalizacion, \
                        i.tipoItem_id,i.estado, i.descripcion, \
                        i.fechaCreacion, i.autorVersion_id, i.idItem)
            sesion.add(histoItem);
            
            i.setValues(i.nombreItem, i.prioridad, i.costo, i.complejidad, i.fechaInicio, i.fechaFinalizacion, \
                        i.tipoItem_id,i.estado, i.descripcion, \
                        i.fechaCreacion, i.autorVersion_id, i.idFase)
            i.version=i.version+1;
            sesion.add(i);
            
            r=sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).all()
            
            for rela in r: #se agrega la relaciones actuales al historial
                histoRel=HistorialRelacion(rela.padre_id, rela.hijo_id, rela.versionHijo)
                rela.versionHijo=rela.versionHijo+1;
                sesion.add(histoRel);
                sesion.merge(rela);
            
            insti=sesion.query(InstanciaTipoItem).filter(InstanciaTipoItem.idItem==i.idItem).all()
            for instancia in insti:
                ie=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for ies in ie:
                    laIE=InstanciaEntero(ies.entero)
                    laIE.version=ies.version+1;
                    laIE.instanciaTipoItem_id=ies.instanciaTipoItem_id;
                    sesion.add(laIE)
                
                iDate=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for dateInst in iDate:
                    laF=InstanciaFecha(dateInst.fecha)
                    laF.version=dateInst.version+1;
                    laF.instanciaTipoItem_id=dateInst.instanciaTipoItem_id;
                    sesion.add(laF)
                
                iNum=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for numInst in iNum:
                    laN=InstanciaNumerico(numInst.numerico)
                    laN.version=numInst.version+1;
                    laN.instanciaTipoItem_id=numInst.instanciaTipoItem_id;
                    sesion.add(laN)
                
                iCad=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for cadInst in iCad:
                    caN=InstanciaCadena(cadInst.cadena)
                    caN.version=cadInst.version+1;
                    caN.instanciaTipoItem_id=cadInst.instanciaTipoItem_id;
                    sesion.add(caN)
            
        elif(i.version==int(version_hijo)): #esta en la misma sesion debe agregar nada mas sin crear nuevo item en el historial
                #nada, se agrega nada mas 
                2+2; 
        else: 
                return make_response('t,Nro de version invalido enviado')
            
        rel=Relacion(padre_id, hijo_id, version_hijo);
        sesion.add(rel)
        sesion.commit()
        sesion.close()
        return make_response('f,Items relacionados correctamente')

    