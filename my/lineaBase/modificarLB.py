import flask.views
from utils import login_required,controlRol
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
        """
        Metodo utilizado para recibir los datos de una linea base cuyos valores
        corresponden a los nuevos valores que tomara esa linea base en el sistema. 
        Invocado cuando se hace una peticion de modificacion de 
        linea base al servidor.
        @type descripcion : sting
        @param descripcion: descripcion de la linea base a agregar
        @type idLB : string
        @param idLB : id de la linea base a modificar
        @type estado : string
        @param estado : id de la linea base a modificar
        """
        idLb=flask.request.form['idLB']
        descripcion=flask.request.form['descripcion']
        estado=flask.request.form['estado']
        
        sesion=Session()
        l=sesion.query(LineaBase).filter(LineaBase.id==int(idLb)).first()
        if l is None:
            return "t, Linea Base no existe"
        if controlRol(str(l.idFase),'lb','administrar')==0:
            return "t, No posee permiso para realizar esta accion"
        
        
        if estado=="cerrada":
            return "t,La linea Base se ha cerrado. No puede modificarse"
        lb=LineaBase(descripcion,estado)
        lb.descripcion=lb.descripcion.strip()
        lb.estado=lb.estado.strip()
        idLb=idLb.strip()
        lbc=LBControllerClass()
        
        return lbc.controlarLB(lb, idLb)
    
