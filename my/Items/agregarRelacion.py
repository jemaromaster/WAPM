
import flask.views
from flask import make_response
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from models.bdCreator import Session

from Grafos.nodo import Nodo
sesion=Session()
class AgregarRelacion(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de \
    usuario al servidor. \Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo \
    Atributos de la clase: id, nombre, fecha inicio, fecha finalizacion, descripcion, estado, proyecto
    """
    
    @login_required
    def post(self):
        
        idFase=flask.request.form['id_Fase']
        padre_id=flask.request.form['padre_id']
        hijo_id=flask.request.form['hijo_id']
        
        #se realiza el control
        if(padre_id==hijo_id):
            return make_response('t,No se puede relacionar el item con el mismo item')
        
        q=sesion.query(Relacion).filter(Relacion.padre_id==padre_id).filter(Relacion.hijo_id==hijo_id).first();
        
        if(q is not None):
            return make_response('t,Ya existe esa relacion')
        
        q=sesion.query(Relacion).filter(Relacion.padre_id==hijo_id).filter(Relacion.hijo_id==padre_id).first();
        
        if(q is not None):
            return make_response('t,Ya existe la relacion inversa, genera una relacion circular')
        
        qp=sesion.query(Item).filter(Item.idItem==padre_id).first()
        qs=sesion.query(Item).filter(Item.idItem==hijo_id).first()
        
        if(qp is not None and qs is not None):
            if qp.idFase>qs.idFase:
                return make_response('t,No puede relacionar un item de una Fase posterior con una fase Anterior')
        
        
        if(qs.estado!="activo"):
            return make_response('t,Solamente puede relacionarse items con estado activo')
        
        q=sesion.query(Item).filter(Item.idFase==int(idFase)).filter(Item.estado=='activo').all()
        
        nLista=dict()
        #aca se crea el grafo
        p=None;
        h=None;
        for i in q:
            aux=Nodo(i.idItem, i.idFase);
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
            return make_response('t,La relacion tiene ciclos')
        
        rel=Relacion(padre_id, hijo_id);
        sesion.add(rel)
        sesion.commit()
        
        return make_response('f,Items relacionados correctamente')
    
        
            
        
        