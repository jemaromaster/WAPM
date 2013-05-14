import flask
import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto 
from proyectoController import ProyectoControllerClass
from models.bdCreator import Session

class ModificarProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def get(self):
        """
        prueba
        """
        return "nada"
    
    @login_required
    def post(self):
        idProyecto=flask.request.form['idProyecto']
        nombreProyecto=flask.request.form['nombreProyecto']
        idProjectLeader=flask.request.form['idProjectLeader']
        observacion=flask.request.form['observacion']
        presupuesto=flask.request.form['presupuesto']
        fechaInicio=flask.request.form['fechaInicio']
        fechaFinalizacion=flask.request.form['fechaFinalizacion']
        estado=flask.request.form['estado']
        
        '''se intercambia de orden de la fecha de DMY a MDY'''
        '''
        fechaInicio=fechaInicio[3:5]+'/'+fechaInicio[0:2]+'/'+fechaInicio[6:10]
        fechaFinalizacion=fechaFinalizacion[3:5]+'/'+fechaFinalizacion[0:2]+'/'+fechaFinalizacion[6:10]
        '''
        print fechaInicio
        print fechaFinalizacion
       
        u=Proyecto(nombreProyecto, idProjectLeader, fechaInicio, \
                   fechaFinalizacion, \
                   presupuesto, observacion, estado)
        
        
        # cu=UsuarioControllerClass()
        #retorno=cu.controlarUsuario(u)
        
        
        pc=ProyectoControllerClass()
        
        return pc.controlarProyecto(u, idProyecto)