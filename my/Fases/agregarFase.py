
import flask.views
from utils import login_required
from models.faseModelo import Fase
from Fases.faseController import FaseControllerClass;



class AgregarFase(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    Atributos de la clase: id, nombre, fecha inicio, fecha finalizacion, descripcion, estado, proyecto
    """
    
    @login_required
    def get(self):
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
    
        nombreFase=flask.request.form['nombreFase']
        fechaInicio=flask.request.form['fechaInicio']
        fechaFinalizacion=flask.request.form['fechaFinal']
        descripcion=flask.request.form['descripcion']
        estado="desarrollo"
        idProyecto=flask.request.form['idProyecto']
        '''
        fechaInicio=fechaInicio[3:5]+'/'+fechaInicio[0:2]+'/'+fechaInicio[6:10]
        fechaFinalizacion=fechaFinalizacion[3:5]+'/'+fechaFinalizacion[0:2]+'/'+fechaFinalizacion[6:10]
        '''  
        f=Fase(nombreFase, descripcion, estado,fechaInicio, fechaFinalizacion,   idProyecto)
        
       
        fc=FaseControllerClass()
        
        return fc.controlarFase(f, 0)
    
        
            
        
        
               
