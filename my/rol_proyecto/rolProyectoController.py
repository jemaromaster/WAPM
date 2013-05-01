from flask import views, make_response
import flask.views
from models.rolProyectoModelo import RolProyecto 
from models.bdCreator import Session

from rolProyectoManejador import RolProyectoManejador

class RolProyectoControllerClass(flask.views.MethodView):
    
    def controlarRolProyecto(self,rol,idRol):
        if len(rol.nombre) <= 0 or len(rol.nombre) > 20:
            return make_response("f,Nombre del Rol incorrecto")
        if len(rol.descripcion) <= 0 or len(rol.descripcion) > 50:
            return make_response("f,Descripcion del Rol incorrecto")
        rm=RolProyectoManejador()    
        return rm.guardarRolProyecto(rol, idRol)
            