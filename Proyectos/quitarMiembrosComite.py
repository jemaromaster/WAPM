import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from models.solicitudCambioModelo import SolicitudCambio
from Proyectos.proyectoController import ProyectoControllerClass
from models.bdCreator import Session


class QuitarMiembrosComite(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de sacar a 
    un usuario como miembro de comite de un proyecto al servidor.
    Los metodos get y post indican como debe comportarse la clase
     segun el tipo de peticion que se realizo 
    """
    
    @login_required
    def post(self):
    
        idProyecto=flask.request.form['idProyecto']
        
        idUsuario=flask.request.form['idUsuario']
        
        try:
            idProyecto=int(idProyecto)
            idUsuario=int(idUsuario)
        except:
            return "t,No se puede convertir a entero proyecto o usuario" 
        
        sesion=Session()
        
        control = sesion.query(Usuario).filter(SolicitudCambio.idProyecto==idProyecto,SolicitudCambio.estado=="pendiente").count()
        if control > 0:
            sesion.close()
            return "t, Se esta realizando el proceso de votacion en una o mas solicitudes, no se puede modificar el comite"
        
        
        
        user=sesion.query(Usuario).filter(Usuario.id==int(idUsuario)).first()
        proyecto= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
        
        try:
            proyecto.usuariosComite.remove(user)
        except:
            sesion.close()
            return "t,No se puede extraer del Comite a un usuario que no es miembro"
        
        sesion.add(proyecto)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,Usuario eliminado correctamente del proyecto" 
    
        
            