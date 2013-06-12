import flask.views
from utils import login_required,controlRol
from models.lineaBaseModelo import LineaBase
from LBController import LBControllerClass;
from models.bdCreator import Session
import json


class AgregarLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    Linea Base al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos con los que se creara una Linea Base nueva dentro
        de algun proyecto. Invocado cuando se hace una peticion de creacion de 
        linea base al servidor.
        @type descripcion : sting
        @param descripcion: descripcion de la linea base a agregar
        @type idFase : string
        @param idFase : id de la fase a la que corresponde la Linea base a agregar
        
        """
        descripcion=flask.request.form['descripcion']
        idFase=flask.request.form['idFase']
        estado="abierta"
        lb=LineaBase(descripcion,estado)
        
        lb.idFase=idFase
        lb.descripcion=lb.descripcion.strip()
        lb.idFase=lb.idFase.strip()
        
        if controlRol(str(idFase),'lb','administrar')==0:
            return "t, No posee permiso para realizar esta accion"
        
        lbc=LBControllerClass()
        
        return lbc.controlarLB(lb, 0)