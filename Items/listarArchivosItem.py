from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date
from models.usuarioModelo import Usuario
from models.itemModelo import Item
from models.archivosModelo import Archivos
sesion=Session()

class ListarArchivosItem(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de listado de 
    archivos al servidor. 
    """
    
    def format_fecha(self, fecha):
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    def jasonizar(self, v):
        """
        Modulo que jasoniza la respuesta.
        @type  v: Query[]
        @param v: Resultado de una consulta que trae el archivo 
        """
        cad=''
        pre='['
        
        if(v is not None):
            for iv in v:
                cad=cad+json.dumps({"idArchivo":iv.idArchivo, "nombreArchivo":iv.nombreArchivo}, separators=(',',':'));
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
            cad=pre + cad+"]"    
        else: 
            cad='t,No existe en el sistema archivos para ese item'
        return cad 
    
    @login_required
    def get(self): 
        """
        Recibe la peticion de listar archivos, segun los parametros que incluya la peticion.
        @type idItem: String
        @param idItem: id del item del cual listar los archivos 
        """ 
        #se obtiene los datos de post del server
        idItem=flask.request.args.get('idItem', '')
        
        iV=sesion.query(Archivos).filter(Archivos.item_id==int(idItem)).all()
        #print(str(sesion.query(Archivos).filter(Archivos.item_id==int(idItem)).count()))
        respuesta=self.jasonizar(iV)
        sesion.close()
        return respuesta
        