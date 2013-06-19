
import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from proyectoController import ProyectoControllerClass
import datetime
from datetime import date

class AgregarProyecto(flask.views.MethodView):
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
    
        nombreProyecto=flask.request.form['nombreProyecto']
        idProjectLeader=flask.session['idUsuario']
        observacion=flask.request.form['observacion']
        presupuesto=flask.request.form['presupuesto']
        fechaInicio=None
        fechaFinalizacion=None
        estado=flask.request.form['estado']
        
        u=Proyecto(nombreProyecto, idProjectLeader, fechaInicio, \
                   fechaFinalizacion, \
                   presupuesto, observacion, estado)
        
        # cu=UsuarioControllerClass()
        #retorno=cu.controlarUsuario(u)
        
        
        pc=ProyectoControllerClass()
        
        return pc.controlarProyecto(u,0)
    
        
            
        
        
               
