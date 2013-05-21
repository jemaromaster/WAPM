import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from Proyectos.proyectoController import ProyectoControllerClass
from models.bdCreator import Session


class AgregarMiembrosProyecto(flask.views.MethodView):
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
        print 'Se busca ' + str(idProyecto)
        idUsuario=flask.request.form['idUsuarioAgregar']
        
        sesion=Session()
        user=sesion.query(Usuario).filter(Usuario.id==idUsuario).first()
       
        if(idProyecto!=0):
            p=sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
            if(user in p.usuariosMiembros):
                sesion.close()
                return "t,Usuario ya existe en proyecto" 
            else:
                p.usuariosMiembros.append(user)
            sesion.add(p)
            sesion.commit()
        
        sesion.close()
        
       
        return "f,Usuario agregado correctamente al proyecto" 
    
        
            