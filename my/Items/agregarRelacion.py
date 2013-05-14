
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
        rel=Relacion(padre_id, hijo_id);
        sesion.add(rel)
        sesion.commit()
        
        return make_response('f,Items relacionados correctamente')
    
        
            
        
        