import flask
import flask.views
from utils import login_required
from models.faseModelo import Fase 
from faseController import FaseControllerClass
from models.bdCreator import Session

class ModificarFase(flask.views.MethodView):
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
        idFase=flask.request.form['idFase']
        nombreFase=flask.request.form['nombreFase']
        fechaInicio=flask.request.form['fechaInicio']
        fechaFinalizacion=flask.request.form['fechaFinal']
        descripcion=flask.request.form['descripcion']
        estado=flask.request.form['estado']
        idProyecto=flask.request.form['idProyecto']
        
        '''se intercambia de orden de la fecha de DMY a MDY'''
        
        fechaInicio=fechaInicio[3:5]+'/'+fechaInicio[0:2]+'/'+fechaInicio[6:10]
        fechaFinalizacion=fechaFinalizacion[3:5]+'/'+fechaFinalizacion[0:2]+'/'+fechaFinalizacion[6:10]
        
        f=Fase(nombreFase, descripcion, estado,fechaInicio, fechaFinalizacion,   idProyecto)
        
        
        fc=FaseControllerClass()
        
        return fc.controlarFase(f, idFase)
    