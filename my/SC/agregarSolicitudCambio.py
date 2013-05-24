import flask.views
from flask import make_response
from utils import login_required

from models.solicitudCambioModelo import SolicitudCambio
from models.itemModelo import Item
from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto
from models.solicitudCambioModelo import Voto

from models.bdCreator import Session
import json


class AgregarSolicitudCambio(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    solicitud de cambio al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        
        idProyecto=flask.request.form['idProyecto'] 
        idSolicitante=flask.request.form['idSolicitante']
        descripcion=flask.request.form['descripcion']
        estado="pendiente"
        itemsJSON=flask.request.form['items']
        listaItem=json.loads(itemsJSON)
        
        idProyecto=idProyecto.strip()
        idSolicitante=idSolicitante.strip()
        descripcion=descripcion.strip()
        
        #controles
        if idProyecto == '0' or idProyecto== '' or idProyecto is None:
            return make_response('t,Proyecto no valido')
        if idSolicitante == '0' or idSolicitante== '' or idSolicitante is None:
            return make_response('t,Usuario Solicitante no valido')
        lenD = len(descripcion)
        if lenD <=0 or lenD > 50:
            return make_response('t,Descripcion de Motivo no valida')
        lenD= len (listaItem)
        if lenD <=0:
            return make_response('t,Debe incluir items en la solicitud')
            
        SC=SolicitudCambio(descripcion,estado)
        SC.idSolicitante=idSolicitante
        SC.idProyecto=idProyecto
        
        sesion=Session()
        
        for idItem in listaItem:
            id=int(idItem)
            item=sesion.query(Item).filter(Item.idItem==id).first()
            SC.items.append(item)
        
        comite=sesion.query(Usuario).join(Proyecto.usuariosComite).filter(Proyecto.idProyecto==int(idProyecto)).all()
        i=0
        #sesion.add(SC)
        voto=Voto()
        for miembro in comite:
            
            
            voto.solicitud=SC.id
            voto.votante=miembro.id
            voto.voto="p"
            SC.votos.append(voto)
            #sesion.add(voto)
        sesion.add(SC)    
        sesion.commit()
        sesion.close()        
        return make_response('f,Solicitud creada con Exito!')
    
        
            
        
        
               
