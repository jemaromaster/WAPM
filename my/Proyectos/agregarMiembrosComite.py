import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from Proyectos.proyectoController import ProyectoControllerClass
from models.bdCreator import Session


class AgregarMiembrosComite(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de agregar a 
    un usario dentro del comite de aprobacion del proyecto. 
    Los metodos get y post indican como debe comportarse la 
    clase segun el tipo de peticion que se realizo 
    """
    @login_required
    def post(self):
    
        idProyecto=flask.request.form['idProyecto']
        idUsuario=flask.request.form['idUsuario']
        
        sesion=Session()
        user=sesion.query(Usuario).filter(Usuario.id==idUsuario).first()
       
        if(idProyecto==0):
            sesion.close()
            return "t,Proyecto no existe"
        
        p=sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
        
        if(user not in p.usuariosMiembros):
            sesion.close()
            return "t,Usuario no pertenece al proyecto" 
        
        if(user in p.usuariosComite):
            sesion.close()
            return "t,Usuario ya forma parte del comite"
        
        p.usuariosComite.append(user)
        sesion.add(p)
        sesion.commit()
        sesion.close()
        
       
        return "f,Usuario agregado correctamente como miembro del Comite" 
    
        
            