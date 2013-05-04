import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from models.usuarioModelo import Usuario
from models.bdCreator import Session


class QuitarRolUsuario(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de sacar un
    permiso de un rol de proyecto al servidor. Los metodos 
    get y post indican como debe comportarse la clase segun 
    el tipo de peticion que se realizo 
    """
    @login_required
    def post(self):
    
        idRol=flask.request.form['idRol']
        idUsuario=flask.request.form['idUsuario']
        
        try:
            idRol=int(idRol)
            idUsuario=int(idUsuario)
        except:
            return "t,Rol o Usuario incorrectos" 
        
        sesion=Session()
        rol=sesion.query(RolProyecto).filter(RolProyecto.id==idRol).first()
        usuario= sesion.query(Usuario).filter(Usuario.id==idUsuario).first()
        
        try:
            usuario.roles_proyecto.remove(rol)
        except:
            return "t,El rol seleccionado no se encuentra asignado al Usuario"
        
        sesion.add(usuario)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,Rol extraido" 
    
        
            