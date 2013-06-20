import flask.views
from utils import login_required,controlRol
from models.tipoItemModelo import TipoItem
from models.atributosModelo import Atributos
from TipoItemController import TipoItemControllerClass;
from models.bdCreator import Session
from models.rolSistemaModelo import RolSistema
from models.faseModelo import Fase
import json
from flask import make_response 

from models.bdCreator import Session
sesion=Session()
class InactivarTipoItem(flask.views.MethodView):
    """
    Clase utilizada al realizar una peticion de creacion de Tipo de Items.\
    Los metodos get y post indican como\
    debe comportarse la clase segun el tipo de peticion que \
    se realizo 
    """
    @login_required
    def get(self):
        return 'nada'
    
    @login_required
    def post(self):
        
        idTI=flask.request.form['idTI']
        
        q=sesion.query(TipoItem).filter(TipoItem.idTipoItem==int(idTI)).first()
        
        if(q is not None):
            if controlRol(str(q.fase_id),'tipo','administrar')==0:
                return "t, No posee permiso para realizar esta accion"
            q.estado='inactivo'
            sesion.merge(q)
            sesion.commit()
            sesion.close()
        else:
            sesion.close()
            return make_response("t, No existe el tipo de item ")
            
        return make_response("f, Tipo de Item inactivado correctamente ")
    
        
            
        
        
               
