import flask.views
from utils import login_required
from models.tipoItemModelo import TipoItem
from models.atributosModelo import Atributos
from TipoItemController import TipoItemControllerClass;
from models.bdCreator import Session
from models.rolSistemaModelo import RolSistema
import json


class ModificarTipoItem(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def get(self):
        return 'nada'
    
    @login_required
    def post(self):
        
        idTipoItem=flask.request.form['idTipoItem']
        nombreTI=flask.request.form['nombreTipoItem']
        estado=flask.request.form['estado']
        descripcion=flask.request.form['descripcion']
        atributos=json.loads(flask.request.form['atributos'])
        idProyecto=flask.request.form['idProyecto']
        idFase=flask.request.form['idFase']
        
        
        #  [{"idAtributos":"1","nombreAtributo":"sada","tipoPrimario":"Texto","longitudCadena":"12"},
        #   {"idAtributos":"2","nombreAtributo":"wad","tipoPrimario":"Texto","longitudCadena":"2"}]
        ti=TipoItem(nombreTI,descripcion, estado)
        tic=TipoItemControllerClass();
        return tic.controlarTI(ti, idTipoItem, atributos, idProyecto, idFase)
    
        
            
        
        
               
