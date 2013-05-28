
import flask.views
from utils import login_required
from utils import rolPL_required
from models.faseModelo import Fase
from Fases.faseController import FaseControllerClass;



class AgregarFase(flask.views.MethodView):
    """Clase utilizada cuando se hace una peticion de creacion de 
    fase al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo """
    
    @login_required
    @rolPL_required
    def get(self):
        return "<h1>no existe el contenido<h1>"
    
    @login_required
    @rolPL_required
    def post(self):
        """
        Metodo utilizado para recibir los datos con los que se creara una fase nueva dentro
        de algun proyecto. Invocado cuando se hace una peticion de creacion de 
        fase al servidor.
        @type  nombreFase: String
        @param nombreFase: nombre de la fase a agregar
        @type  fechaInicio: date
        @param fechaInicio: fecha de inicio de la fase
        @type  fechaFinal: date
        @param fechaFinal: fecha de finalizacion de la fase
        @type  descripcion: String
        @param descripcion: una descripcion de la fase
        @type  idProyecto: String
        @param idProyecto: el id del proyecto al cual la fase pertenecera
        """
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