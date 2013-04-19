import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from proyectoController import ProyectoControllerClass
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
    
        '''idProyecto=flask.request.form['idProyecto']
        idProyecto='1'
        idUsuario=flask.session['idUsuario']
        idUsuario='1'
        sesion=Session()
        
        if(idProyecto!=0):
            p=sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).first()
            p.setMiembrosProyecto(idUsuario)
            sesion.add(p)
            sesion.commit()
        
        sesion.close()'''
        
       
        return "f,Usuario agregado correctamente al proyecto" 
    
        
            