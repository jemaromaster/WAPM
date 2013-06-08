
import flask.views
from flask import make_response
from utils import login_required,controlRol
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
    Clase utilizada cuando se hace una peticion de \
    eliminar, revivir o aprobar un item  al servidor. 
    
    """
    
    @login_required
    def get(self):
        sesion.close()
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos para eliminar, revivir o aprobar item en la base de datos. 
        @type  idItem: string
        @param idItem: id del item en BD
        @type  idFase: string
        @param idFase: id de la fase del item
        @type  accion: string
        @param accion: Permite definir si es un eliminar, revivir o aprobacion 
        """
        idItem=flask.request.form['idItem']
        idFase=flask.request.form['idFase']
        accion=flask.request.form['accion']
        
        q=sesion.query(Item).filter(Item.idItem==idItem).first();
        msg=""
        if(accion=="eliminar"):
            
            if controlRol(idFase,'item','administrar')==0:
                sesion.close()
                return "t, No posee permiso para realizar esta accion"
            
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
            
                if controlRol(idFase,'item','administrar')==0:
                    sesion.close()
                    return "t, No posee permiso para realizar esta accion"
            
                q.estado='activo'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,Se ha revivido correctamente al item'
        elif(accion=="aprobar"):
            
            if controlRol(idFase,'item','finalizar')==0:
                sesion.close()
                return "t, No posee permiso para realizar esta accion"
            
            bandera=0;
            listaPadres='';
            contador=sesion.query(Relacion).filter(Relacion.hijo_id==q.idItem).count()
            f=sesion.query(Fase).filter(Fase.idFase==q.idFase).first()
            if(f.tag!="F1" and contador==0): #si no esta en la primera fase y contador==0
                return make_response('t,No puede aprobarse un item que no tenga por lo menos algun padre')
            
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
            if(q.estado=="activo"):
                
                if controlRol(idFase,'item','finalizar')==0:
                    sesion.close()
                    return "t, No posee permiso para realizar esta accion"
                
                contador=sesion.query(Relacion).filter(Relacion.hijo_id==q.idItem).count()
                
                f=sesion.query(Fase).filter(Fase.idFase==q.idFase).first()
                if(f.tag!="F1" and contador==0): #si no esta en la primera fase y contador==0
                    return make_response('t,No puede pasar a pendiente un item que no tenga por lo menos algun padre')
                q.estado='pendiente'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,Se ha cambiado correctamente el estado del item de "activo" a "pendiente"'
            elif(q.estado=="pendiente"):
                if controlRol(idFase,'item','finalizar')==0:
                    sesion.close()
                    return "t, No posee permiso para realizar esta accion"
                q.estado='activo'
                sesion.merge(q)
                sesion.commit()
                sesion.close()
                msg='f,Se ha cambiado correctamente el estado del item de "pendiente" a "activo"'
            
        else:
            sesion.close()
            return make_response('t,accion invalida ')
        return make_response(msg)
    
        
            
        
        
               
