import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from models.permisoModelo import Permiso
from models.bdCreator import Session


class QuitarPermisoRol(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de sacar un
    permiso de un rol de proyecto al servidor. Los metodos 
    get y post indican como debe comportarse la clase segun 
    el tipo de peticion que se realizo 
    """
    @login_required
    def post(self):
    
        idRol=flask.request.form['idRol']
        
        idPermiso=flask.request.form['idPermiso']
        
        try:
            idRol=int(idRol)
            idPermiso=int(idPermiso)
        except:
            return "t,No se puede convertir a entero rol o permiso" 
        
        sesion=Session()
        permiso=sesion.query(Permiso).filter(Permiso.id==idPermiso).first()
        rol= sesion.query(RolProyecto).filter(RolProyecto.id==idRol).first()
        if rol.estado== "activo":
                return "t,El rol no puede ser modificado. Ya se encuentra activo"
        
        try:
            rol.permisos.remove(permiso)
        except:
            return "t,El permiso seleccionado no se encuentra en el Rol"
        
        sesion.add(rol)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,Permiso eliminado correctamente del rol" 
    
        
            