import flask.views
from utils import login_required,controlRol
from models.lineaBaseModelo import LineaBase
from models.itemModelo import Item
from models.bdCreator import Session


class AgregarItemLB(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion al servidor para 
    agregar un item a una linea base del proyecto. Los metodos get y post 
    indican como debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos de un item a ser agregado dentro
        de una linea base.
        @type idLB: string
        @param idLB: id de la linea base a la cual se le agregara el item
        @type idItem: string
        @param idItem :id del item a agregar
        """
        idLB=flask.request.form['idLB']
        idItem=flask.request.form['idItem']
        
        sesion=Session()
        item=sesion.query(Item).filter(Item.idItem==idItem).first()
        idFase=str(item.idFase)
        if controlRol(idFase,'lb','administrar')==0:
            sesion.close()
            return "t, No posee permiso para realizar esta accion"
                   
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
        
            