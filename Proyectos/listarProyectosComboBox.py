from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    proyectos al servidor. Se obtienen de la bd las filas a 
    devolver dentro de la lista y se convierte a un formato
    json para que pueda ser interpretado por el navegador 
    """
    totalPages=1
    currPage=1
    totalRecords=1
    rows=1
    
    def __init__(self, totalPages,currPage,totalRecords,rows):
        self.totalPages=totalPages
        self.currPage=currPage
        self.totalRecords=totalRecords
        self.rows=rows
    
    
        
class ListarProyectosComboBox(flask.views.MethodView):
    
    def jasonizar(self, listaProyecto):
        """
        modulo que jasoniza la respuesta
        """
        cad=''
        pre="["
        for proy in listaProyecto:
            cad=cad+ json.dumps({"idProyecto":proy.idProyecto , "nombreProyecto":proy.nombreProyecto}, separators=(',',':'));
            cad=cad + ","
        cad=cad[0:len(cad)-1]    
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
      
        usuarioId=flask.session['idUsuario']
        
        proyectoLista=sesion.query(Proyecto)\
                                                .join((Usuario,Proyecto.usuariosMiembros))\
                                                .filter(Proyecto.estado=='activo') \
                                                .filter(Usuario.id==usuarioId).all()
         
        respuesta=self.jasonizar(proyectoLista)
        sesion.close()
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"