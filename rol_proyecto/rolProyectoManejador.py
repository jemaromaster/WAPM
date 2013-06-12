from models.rolProyectoModelo import RolProyecto  
from models.bdCreator import Session
from flask import make_response

class RolProyectoManejador:
    def guardarRolProyecto(self, rol, idRol):
        sesion=Session()
        r=rol
        if idRol != 0:
            r=sesion.query(RolProyecto).filter(RolProyecto.id==idRol).first()
            r.nombre=rol.nombre;r.descripcion=rol.descripcion;r.estado=rol.estado
            
            
        sesion.add(r)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Rol guardado correctamente")
        
