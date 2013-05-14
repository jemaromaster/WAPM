
import flask.views
from flask import make_response
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item
from models.bdCreator import Session

sesion=Session()
class EliminarItem(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de \
    usuario al servidor. \Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo \
    Atributos de la clase: id, nombre, fecha inicio, fecha finalizacion, descripcion, estado, proyecto
    """
    
    @login_required
    def get(self):
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
        
        idItem=flask.request.form['idItem']
        idFase=flask.request.form['idFase']
        accion=flask.request.form['accion']
        
        q=sesion.query(Item).filter(Item.idItem==idItem).first();
        msg=""
        if(accion=="eliminar"):
            if(q.estado=='inactivo'):
                return make_response('t,El item ya se encuentra eliminado')
            else:
                q.estado='inactivo'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,El item se ha eliminado correctamente'
        elif(accion=="revivir"):
                q.estado='desarrollo'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,Se ha revivido correctamente al item'
        else:
            return make_response('t,accion invalida ')
        return make_response(msg)
    
        
            
        
        
               
