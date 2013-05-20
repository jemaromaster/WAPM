import flask.views
from utils import login_required
from models.lineaBaseModelo import LineaBase
from models.bdCreator import Session


class CerrarLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    agregar un permiso a un rol de proyecto. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
    
        idLB=flask.request.form['idLB']
        
        sesion=Session()
        lb=sesion.query(LineaBase).filter(LineaBase.id==int(idLB)).first()
       
                   
        if(lb.estado=="cerrada"):
            return "t,Linea Base ya se encuentra cerrada"
        if len(lb.items) <= 0:
            return "t,Linea Base no posee items. No puede ser cerrada"
        
        lb.estado="cerrada"
        sesion.add(lb)
        sesion.commit()
        sesion.close()
        
        return "f,Se ha cerrado con exito la Linea Base!" 
    @login_required
    def get(self):
        return "nada"
        
            