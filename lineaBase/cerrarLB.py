import flask.views
from utils import login_required,controlRol
from models.lineaBaseModelo import LineaBase
from models.bdCreator import Session


class CerrarLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    cerrar una linea Base. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos de la linea base a cerrar.
        @type idLB : string
        @param idLb : id de la linea base a ser cerrada
        """
        idLB=flask.request.form['idLB']
        
        sesion=Session()
        lb=sesion.query(LineaBase).filter(LineaBase.id==int(idLB)).first()
        
        if lb is None:
            sesion.close()
            return "t, Linea Base no existe"
        if controlRol(str(lb.idFase),'lb','finalizar')==0:
            sesion.close()
            return "t, No posee permiso para realizar esta accion"
                   
        if(lb.estado!="abierta"):
            sesion.close()
            return "t, No se puede cerrar una Linea Base "+lb.estado
        if len(lb.items) <= 0:
            sesion.close()
            return "t,Linea Base no posee items. No puede ser cerrada"
        
        lb.estado="cerrada"
        sesion.add(lb)
        sesion.commit()
        sesion.close()
        
        return "f,Se ha cerrado con exito la Linea Base!" 
    @login_required
    def get(self):
        return "nada"
        
            