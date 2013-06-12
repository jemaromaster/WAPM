from utils import login_required
import flask.views
from flask import jsonify,json, g, make_response
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.itemModelo import Relacion
from models.usuarioModelo import Usuario
from models.historialModelo import HistorialRelacion
from sqlalchemy import or_

sesion=Session()

class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    proyectos al servidor. Se obtienen de la bd las filas a 
    devolver dentro de la lista y se convierte a un formato
    json para que pueda ser interpretado por el navegador 
    """
    
    def __init__(self, totalPages,currPage,totalRecords,rows):
        self.totalPages=totalPages
        self.currPage=currPage
        self.totalRecords=totalRecords
        self.rows=rows
    
    

class ListarRelacionesEnFase(flask.views.MethodView):
    def jasonizar(self, listaRel):
        
        p=''
        pre="["
        for f in listaRel:
            p=p+json.dumps({"idRelacion": f.idRelacion , "idHijo":f.hijo_id,  \
                            "idPadre": f.padre_id}, separators=(',',':'))+",";
        p=p[0:len(p)-1]    
        p=p+"]"    
        p=pre+p
        return p 
        

    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        idProyecto=int(flask.request.args.get('idP', ''))
        idFase=int(flask.request.args.get('idF', ''))
        
        
        if(int(idFase)==0):
            return make_response ("f,No se ha enviado suficiente informacion")
        
        listaItemEnFase=sesion.query(Item.idItem).filter(Item.idFase==idFase).all()
        listaRel=sesion.query(Relacion).filter(or_(Relacion.hijo_id.in_(listaItemEnFase), Relacion.padre_id.in_(listaItemEnFase)))\
                                                    .distinct()
       
            
       
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=self.jasonizar(listaRel)
        sesion.close()
        return respuesta
        
        