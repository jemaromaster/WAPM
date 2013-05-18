import flask.views
from utils import login_required
from models.lineaBaseModelo import LineaBase
from LBController import LBControllerClass;
from models.bdCreator import Session
import json


class ModificarLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    Linea Base al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        idLb=flask.request.form['idLB']
        descripcion=flask.request.form['descripcion']
        estado=flask.request.form['estado']
        if estado=="cerrada":
            return "t,La linea Base se ha cerrado. No puede modificarse"
        lb=LineaBase(descripcion,estado)
        lb.descripcion=lb.descripcion.strip()
        lb.estado=lb.estado.strip()
        idLb=idLb.strip()
        lbc=LBControllerClass()
        
        return lbc.controlarLB(lb, idLb)
    
