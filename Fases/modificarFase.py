import flask
import flask.views
from utils import login_required
from utils import rolPL_required
from models.faseModelo import Fase 
from faseController import FaseControllerClass
from models.bdCreator import Session

class ModificarFase(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    Fase al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    @rolPL_required
    def get(self):
        """
        prueba
        """
        return "nada"
    
    @login_required
    @rolPL_required
    def post(self):
        """
        Metodo utilizado para recibir los datos de una fase cuyos valores
        corresponden a los nuevos valores que tomara esa fase en el sistema. 
        Invocado cuando se hace una peticion de modificacion de 
        fase al servidor.
        @type  idFase: String
        @param idFase: id de la fase a ser modificada
        @type  nombreFase: String
        @param nombreFase: nombre de la fase a agregar
        @type  fechaInicio: date
        @param fechaInicio: fecha de inicio de la fase
        @type  fechaFinal: date
        @param fechaFinal: fecha de finalizacion de la fase
        @type  descripcion: String
        @param descripcion: una descripcion de la fase
        @type  estado: String
        @param estado: el estado en que se encuentra la fase
        @type  idProyecto: String
        @param idProyecto: el id del proyecto al cual la fase pertenecera
        
        """
        idFase=flask.request.form['idFase']
        nombreFase=flask.request.form['nombreFase']
        fechaInicio=None
        fechaFinalizacion=None
        descripcion=flask.request.form['descripcion']
        estado=flask.request.form['estado']
        idProyecto=flask.request.form['idProyecto']
        
        f=Fase(nombreFase, descripcion, estado,fechaInicio, fechaFinalizacion,   idProyecto)
        
        
        fc=FaseControllerClass()
        
        return fc.controlarFase(f, idFase)
    