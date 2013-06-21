from flask import views, make_response
import flask.views
from models.rolProyectoModelo import RolProyecto 
from models.bdCreator import Session
from models.proyectoModelo import Proyecto
from models.faseModelo import Fase

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
        if idRol != 0:
            rolFase=sesion.query(RolProyecto).filter(RolProyecto.id==int(idRol)).first()
            rol.idFase=rolFase.idFase
        
        if rol.idFase == '' or rol.idFase=='0':
            sesion.close()
            return make_response("t,Fase no valida. No se pudo crear el rol")
        rol.idFase=int(rol.idFase)
        
        proyectoId=sesion.query(Fase.idProyecto).filter(Fase.idFase==rol.idFase).first()
        
        controlNombre=sesion.query(RolProyecto).join(Fase).filter(RolProyecto.nombre==rol.nombre).filter(Fase.idProyecto==proyectoId.idProyecto).first()
        if idRol==0:    
            if controlNombre is not None:
                sesion.close()
                return make_response("t,Nombre del Rol ya existe")
        else:
            
            if controlNombre is not None and controlNombre.id != int(idRol):
                sesion.close()
                return make_response("t,Nombre del Rol ya existe")    
        rm=RolProyectoManejador()
        sesion.close()    
        return rm.guardarRolProyecto(rol, idRol)
            