import flask.views
from utils import login_required,controlRol
from models.tipoItemModelo import TipoItem
from models.atributosModelo import Atributos
from TipoItemController import TipoItemControllerClass;
from models.bdCreator import Session
from models.rolSistemaModelo import RolSistema
import json


class AgregarTipoItem(flask.views.MethodView):
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
        
        nombreTI=flask.request.form['nombreTipoItem']
        estado=flask.request.form['estado']
        descripcion=flask.request.form['descripcion']
        atributos=json.loads(flask.request.form['atributos'])
        idProyecto=flask.request.form['idProyecto']
        idFase=flask.request.form['idFase']
        
        if controlRol(idFase,'tipo','administrar')==0:
            return "t, No posee permiso para realizar esta accion" 
             
        #  [{"idAtributos":"1","nombreAtributo":"sada","tipoPrimario":"Texto","longitudCadena":"12"},
        #   {"idAtributos":"2","nombreAtributo":"wad","tipoPrimario":"Texto","longitudCadena":"2"}]
        ti=TipoItem(nombreTI,descripcion, estado)
        tic=TipoItemControllerClass();
        return tic.controlarTI(ti, 0, atributos, idProyecto, idFase)
    
        
            
        
        
               
