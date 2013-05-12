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
    
    
    def format_fecha(self, fecha):
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    def jasonizar(self, iv):
        """
        modulo que jasoniza la respuesta
        """
        cad=''
        
        if(iv is not None):
            name=sesion.query(Usuario.username).filter(Usuario.id==iv.autorVersion_id).first()
            cad=json.dumps({"idItem":iv.idHistorialItem , "nombreItem":iv.nombreItem, "version": iv.version, "prioridad":iv.prioridad, 
                        "fechaInicio": self.format_fecha(str(iv.fechaInicio)), "fechaFinalizacion": self.format_fecha(str(iv.fechaFinalizacion)), 
                        "costo": iv.costo, "complejidad": iv.complejidad, "estado": iv.estado, "autorVersion_id":iv.autorVersion_id,
                        "nombreAutorVersion": name, "descripcion":iv.descripcion}, separators=(',',':'));
        else: 
            cad='t,No existe en el sistema la version solicitada'
        return cad 
    
    @login_required
    def get(self): 
        
        #se obtiene los datos de post del server
        idItem=flask.request.args.get('idItem', '')
        version=flask.request.args.get('version', '')
        
        iV=sesion.query(HistorialItem).filter(HistorialItem.idItemFK==idItem).filter(HistorialItem.version==version).first()
        
        respuesta=self.jasonizar(iV)
        return respuesta
        