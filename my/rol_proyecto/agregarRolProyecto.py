import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from rolProyectoController import RolProyectoControllerClass;
from models.bdCreator import Session
import json


class AgregarRolProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        nombre=flask.request.form['nombre']
        descripcion=flask.request.form['descripcion']
        idFase=flask.request.form['idFase']
        rol=RolProyecto(nombre,descripcion)
        rol.idFase=idFase
       
        rol.nombre=rol.nombre.strip()
        rol.descripcion=rol.descripcion.strip()
        rol.idFase=rol.idFase.strip()
        rpc=RolProyectoControllerClass()
        
        return rpc.controlarRolProyecto(rol, 0)
    
        
            
        
        
               
