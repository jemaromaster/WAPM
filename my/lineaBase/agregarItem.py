import flask.views
from utils import login_required
from models.lineaBaseModelo import LineaBase
from models.itemModelo import Item
from models.bdCreator import Session


class AgregarItemLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    agregar un permiso a un rol de proyecto. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
    
        idLB=flask.request.form['idLB']
        idItem=flask.request.form['idItem']
        
        sesion=Session()
        item=sesion.query(Item).filter(Item.idItem==idItem).first()
       
                   
        if(idLB!=0):
            lb=sesion.query(LineaBase).filter(LineaBase.id==int(idLB)).first()
            lb.items.append(item)
            item.estado="bloqueado"
            sesion.add(lb)
            sesion.add(item)
            sesion.commit()
        
        sesion.close()
        
       
        return "f,Item agregado a Linea Base" 
    @login_required
    def get(self):
        return "nada"
        
            