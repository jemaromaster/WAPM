from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date
from models.usuarioModelo import Usuario
from models.itemModelo import Item
from models.proyectoModelo import Proyecto
from models.historialModelo import HistorialItem
sesion=Session()

class ListarDatosItemVersion(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de los datos una version determinada de un item
    """
    def format_fecha(self, fecha):
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    def jasonizar(self, iv):
        """
        modulo que jasoniza la respuesta
        @type iv:ItemHistorial
        @param iv:objeto de un item en historial 
        """
        cad=''
        
        if(iv is not None):
            name=sesion.query(Usuario.username).filter(Usuario.id==iv.autorVersion_id).first()
            cad=json.dumps({"idItem":iv.idHistorialItem , "nombreItem":iv.nombreItem, "version": iv.version, "prioridad":iv.prioridad, 
                        "costo": iv.costo, "complejidad": iv.complejidad, "estado": iv.estado, "autorVersion_id":iv.autorVersion_id,
                        "nombreAutorVersion": name, "descripcion":iv.descripcion}, separators=(',',':'));
        else: 
            cad='t,No existe en el sistema la version solicitada'
        return cad 
    
    @login_required
    def get(self): 
        """
        Recibe la peticion de listar los atributos de un item del historial, segun los parametros que incluya la peticion.
        @type idItem: String
        @param idItem: id de item del cual listar los valores de atributos 
        @type version: String
        @param version: version del item 
        """ 
        #se obtiene los datos de post del server
        idItem=flask.request.args.get('idItem', '')
        version=flask.request.args.get('version', '')
        
        iV=sesion.query(HistorialItem).filter(HistorialItem.idItemFK==int(idItem)).filter(HistorialItem.version==int(version)).first()
        
        respuesta=self.jasonizar(iV)
        sesion.close()
        return respuesta
        