import flask.views
from utils import login_required
from utils import rolPL_required
from models.permisoModelo import Permiso
from models.rolProyectoModelo import RolProyecto
from models.usuarioModelo import Usuario
from models.bdCreator import Session

class EstadoRol(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de activacion o
    inhabilitacion de un rol al servidor. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de 
    peticion que se realizo 
    """
    @login_required
    @rolPL_required
    def post(self):
        
        idRol=flask.request.form['idRol']
        estado=flask.request.form['estado']
        
        sesion=Session()
        rol= sesion.query(RolProyecto).filter(RolProyecto.id==int(idRol)).first()
        if rol is None:
            sesion.close()
            return "t,No existe Rol"
        if estado == "activo":
            #se debe pasar a inactivo
            cantidad = sesion.query(RolProyecto).filter(RolProyecto.id==idRol).join(RolProyecto.usuarios).count()
            if cantidad > 0:
                sesion.close()
                return "t,No se puede inactivar el Rol. Ya ha sido asignado a usuario/s"
            rol.estado="inactivo"

            sesion.add(rol)
            sesion.commit()
            sesion.close()
            return "f,El Rol ha sido inactivado!" 

            
        else: 
            #se debe pasar a activo
            cantidad = sesion.query(RolProyecto).filter(RolProyecto.id==idRol).join(RolProyecto.permisos).count()
            if cantidad == 0:
                return "t,No se puede activar el Rol. No tiene permisos asignados"
            rol.estado="activo"
            
            sesion.add(rol)
            sesion.commit()
            sesion.close()
            return "f,El rol ha sido activado! Ya no se permitiran modificaciones." 
    
        
            
