import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from models.usuarioModelo import Usuario
from models.bdCreator import Session


class AgregarRolUsuario(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    agregar un permiso a un rol de proyecto. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
    
        idRol=flask.request.form['idRol']
        idUsuario=flask.request.form['idUsuario']
        
        sesion=Session()
        rol=sesion.query(RolProyecto).filter(RolProyecto.id==idRol).first()
        if rol is None:
            return "t,Rol no existe"
        if(idUsuario!=0):
            p=sesion.query(Usuario).filter(Usuario.id==int(idUsuario)).first()
            if p is None:
                return "t,Usuario no existe"
            if(rol in p.roles_proyecto):
                return "t,Rol ya esta asigando al Usuario" 
            else:
                p.roles_proyecto.append(rol)
            sesion.add(p)
            sesion.commit()
        
        sesion.close()
        
       
        return "f,Permiso agregado correctamente al Rol" 
    @login_required
    def get(self):
        return "nada"
        
            