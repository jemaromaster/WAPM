import flask.views
from utils import login_required
from models.rolProyectoModelo import RolProyecto
from models.permisoModelo import Permiso
from models.bdCreator import Session


class AgregarPermisoRol(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    agregar un permiso a un rol de proyecto. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
    
        idRol=flask.request.form['idRol']
        idPermiso=flask.request.form['idPermiso']
        
        sesion=Session()
        permiso=sesion.query(Permiso).filter(Permiso.id==idPermiso).first()
       
        if(idRol!=0):
            p=sesion.query(RolProyecto).filter(RolProyecto.id==int(idRol)).first()
            if(permiso in p.permisos):
                return "t,Permiso ya existe en el Rol" 
            else:
                p.permisos.append(permiso)
            sesion.add(p)
            sesion.commit()
        
        sesion.close()
        
       
        return "f,Permiso agregado correctamente al Rol" 
    @login_required
    def get(self):
        return "nada"
        
            