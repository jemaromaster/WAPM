import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from Proyectos.proyectoController import ProyectoControllerClass
from models.solicitudCambioModelo import SolicitudCambio
from models.bdCreator import Session


class QuitarMiembrosProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    proyecto al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def get(self):
        return flask.render_template('crearProyecto.html')
    
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
        
        control=sesion.query(Usuario).filter(Proyecto.idProyecto==idProyecto).join(Proyecto.usuariosComite)\
                                        .filter(Usuario.id==idUsuario).count()
        if control > 0:
            sesion.close()
            return "t, No se puede sacar al usuario porque es Miembro del Comite"
        
        
        control = sesion.query(Usuario).filter(SolicitudCambio.idProyecto==idProyecto,SolicitudCambio.idSolicitante==idUsuario\
                                        ,SolicitudCambio.estado=="pendiente").count()
        if control > 0:
            sesion.close()
            return "t, No se puede sacar al usuario porque tiene una Solicitud pendiente de aprobacion"
        
        user=sesion.query(Usuario).filter(Usuario.id==int(idUsuario)).first()
        proyecto= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
        
        try:
            proyecto.usuariosMiembros.remove(user)
        except:
            sesion.close()
            return "t,No se puede extraer del proyecto a un usuario que no es miembro"
        
        sesion.add(proyecto)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,Usuario eliminado correctamente del proyecto" 
    
        
            