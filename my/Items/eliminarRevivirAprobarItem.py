
import flask.views
from flask import make_response
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String, or_
from models.itemModelo import Item, Relacion
from models.bdCreator import Session

sesion=Session()
class EliminarRevivirAprobarItem(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de \
    usuario al servidor. \Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo \
    Atributos de la clase: id, nombre, fecha inicio, fecha finalizacion, descripcion, estado, proyecto
    """
    
    @login_required
    def get(self):
        sesion.close()
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
                sesion.close()
                return make_response('t,El item ya se encuentra eliminado')
            else:
                q.estado='inactivo'
                sesion.merge(q)
                sesion.query(Relacion).filter(or_(Relacion.padre_id==q.idItem, Relacion.hijo_id==q.idItem)).delete();
                sesion.commit()
                sesion.close()
                msg='f,El item se ha eliminado correctamente'
        elif(accion=="revivir"):
                q.estado='activo'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,Se ha revivido correctamente al item'
        elif(accion=="aprobar"):
            bandera=0;
            listaPadres='';
            consulta=sesion.query(Item).join(Relacion,Relacion.padre_id==Item.idItem).filter(Item.estado!='inactivo').filter(Relacion.hijo_id==q.idItem).all()
            for p in consulta:
                if(p.estado=='activo' or p.estado=='pendiente'):
                    bandera=bandera+1;
                    listaPadres=listaPadres+p.tag+", "
            
            listaPadres=listaPadres[0:len(listaPadres)-2]
            if (bandera==1):
                sesion.close()
                return make_response('t,El padre del item seleccionado": '+ listaPadres+ ' se encuentra en estado '+ p.estado\
                                     + ' y no puede aprobarse. Es condicion necesaria que todos los padres de un item esten por lo menos en estado "aprobado" para poder aprobarse. ')
            elif(bandera==2):
                sesion.close()
                return make_response('t,Los padres del item seleccionado: '+ listaPadres+ ' no se encuentran en estado de por lo menos aprobado'\
                                     + ' y no puede aprobarse. Es condicion necesaria que todos los padres de un item esten aprobados para poder aprobarse previamente. ')
            q.estado='aprobado'
            sesion.merge(q)
            sesion.commit()
            sesion.close()
            msg='f,Se ha aprobado correctamente al item'
        elif(accion=="pendiente"):
            q.estado='pendiente'
            sesion.merge(q)
            sesion.commit()
            sesion.close()
            msg='f,Se ha cambiado correctamente el estado del item de "activo" a "pendiente"'
        else:
            sesion.close()
            return make_response('t,accion invalida ')
        return make_response(msg)
    
        
            
        
        
               
