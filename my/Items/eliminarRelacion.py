
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
class EliminarRelacion(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de \
    usuario al servidor. \Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo \
    Atributos de la clase: id, nombre, fecha inicio, fecha finalizacion, descripcion, estado, proyecto
    """
    
   
    @login_required
    def post(self):
        
        #idFase=flask.request.form['id_Fase']
        idRelacion=flask.request.form['idRelacion']
        
        #se realiza el control
        
        q=sesion.query(Relacion).filter(Relacion.idRelacion==idRelacion)
        if(q is not None):
            sesion.query(Relacion).filter(Relacion.idRelacion==idRelacion).delete();
        else:
            sesion.close()
            return make_response('t,No existe relacion con ese id')
        
        sesion.commit();
        sesion.close()
        return make_response('f,Items eliminado correctamente')
    
        
            
        
        