import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from rolProyectoController import RolProyectoControllerClass;
from models.bdCreator import Session
import json


class ModificarRolProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    rol de proyecto al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        idRol=flask.request.form['idRol']
        nombre=flask.request.form['nombre']
        descripcion=flask.request.form['descripcion']
        estado=flask.request.form['estado']
        if estado=="activo":
            return "t,El rol esta activo. No puede modificarse"
        rol=RolProyecto(nombre,descripcion,estado)
       
        rol.nombre=rol.nombre.strip()
        rol.descripcion=rol.descripcion.strip()
        rol.estado=rol.estado.strip()
        idRol=idRol.strip()
        rpc=RolProyectoControllerClass()
        
        return rpc.controlarRolProyecto(rol, idRol)
    
