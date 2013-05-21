from flask import views, make_response
import flask.views
from models.rolProyectoModelo import RolProyecto 
from models.bdCreator import Session

from rolProyectoManejador import RolProyectoManejador

class RolProyectoControllerClass(flask.views.MethodView):
    
    def controlarRolProyecto(self,rol,idRol):
        if len(rol.estado) <= 0 or len(rol.estado) > 15:
            return make_response("f,Estado del Rol incorrecto")
        if len(rol.nombre) <= 0 or len(rol.nombre) > 20:
            return make_response("f,Nombre del Rol incorrecto")
        if len(rol.descripcion) <= 0 or len(rol.descripcion) > 50:
            return make_response("f,Descripcion del Rol incorrecto")
        
        sesion=Session()
        controlNombre=sesion.query(RolProyecto).filter(RolProyecto.nombre==rol.nombre).first()
        if idRol==0:    
            if controlNombre is not None:
                sesion.close()
                return make_response("t,Nombre del Rol ya existe")
            if rol.idFase == '' or rol.idFase=='0':
                sesion.close()
                return make_response("t,Fase no valida. No se pudo crear el rol")
            rol.idFase=int(rol.idFase)
        else:
            
            if controlNombre is not None and controlNombre.id != int(idRol):
                sesion.close()
                return make_response("t,Nombre del Rol ya existe")    
        rm=RolProyectoManejador()
        sesion.close()    
        return rm.guardarRolProyecto(rol, idRol)
            