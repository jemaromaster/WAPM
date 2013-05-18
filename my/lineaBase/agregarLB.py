import flask.views
from utils import login_required
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
        descripcion=flask.request.form['descripcion']
        idFase=flask.request.form['idFase']
        estado="abierta"
        lb=LineaBase(descripcion,estado)
        
        lb.idFase=idFase
        lb.descripcion=lb.descripcion.strip()
        lb.idFase=lb.idFase.strip()
        
        lbc=LBControllerClass()
        
        return lbc.controlarLB(lb, 0)