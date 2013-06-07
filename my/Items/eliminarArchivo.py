
import flask.views
from flask import make_response
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from models.historialModelo import HistorialItem, HistorialRelacion
from models.bdCreator import Session
from models.instanciaAtributos import InstanciaNumerico, InstanciaCadena, InstanciaEntero, InstanciaFecha, InstanciaTipoItem
from models.archivosModelo import Archivos
from Grafos.nodo import Nodo
sesion=Session()
class EliminarArchivo(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de \
    eliminacion de archivo al servidor. 
    
    """
    
    @login_required
    def post(self):
            """
            Metodo utilizado para recibir los datos para la eliminacion del archivo en la base de datos. 
            @type  idArchivo: string
            @param idArchivo: id del archivo dentro de la BD 
          
            """ 
            idArchivo=flask.request.form['idArchivo']
            
            if idArchivo is not None:
                a=sesion.query(Archivos).filter(Archivos.idArchivo==int(idArchivo)).count()
               
                
                if a==1:
                    sesion.query(Archivos).filter(Archivos.idArchivo==int(idArchivo)).delete()
                    sesion.commit()
                    sesion.close()
                    return make_response('f,Archivo eliminado correctamente')
                else:
                    return make_response('t,No existe archivo con ese ID')
            else:
                return make_response('t,No se envio el idArchivo')
            
    
        