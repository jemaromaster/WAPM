import flask.views 
from flask import make_response
from utils import login_required
from models.tipoItemModelo import TipoItem
from models.faseModelo import Fase
from models.atributosModelo import Atributos
from TipoItemController import TipoItemControllerClass;
from models.bdCreator import Session
from models.rolSistemaModelo import RolSistema

import json


class ImportarTipoItem(flask.views.MethodView):
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
        
        '''Le paso id del tipo de item que importare y el id de la fase a la cual se importara el tipo'''
        idTipo=flask.request.form['idTipo']
        idFase=flask.request.form['idFase']
        sesion=Session()
        ''' obtengo el tipo de item a importar'''
        importado=sesion.query(TipoItem).filter(TipoItem.idTipoItem==int(idTipo)).first()
        ''' busco si en la fase a importar ya existe un tipo con el mismo nombre, en caso afirmativo, se lanza una excepcion'''
        tipit=sesion.query(TipoItem).filter(TipoItem.fase_id==int(idFase)).filter(TipoItem.nombreTipoItem==importado.nombreTipoItem).first()
        if(tipit is not None):
            sesion.close()
            return make_response('t,Ya existe el tipo de item con ese nombre en esa fase')
        
        ''' se crea el tipo nuevo'''
        nuevoTipo=TipoItem(importado.nombreTipoItem,importado.descripcion,'inactivo')
        atributos=importado.atributosItem
        nuevoAtributos=[]
        '''extraigo todos los atributos del item importado y los meto en una lista para agregar dicha lista
        de atributos al nuevo Tipo'''
        for atributo in atributos:
            '''Pongo en None el id porque necesito que sea autogenerado'''            
            att=Atributos(None,atributo.nombreAtributo,atributo.tipoPrimarioId,atributo.longitudCadena)
            nuevoAtributos.append(att)
        nuevoTipo.atributosItem=nuevoAtributos
        nuevoTipo.fase_id=idFase
        sesion.add(nuevoTipo)
        sesion.commit()
        sesion.close()
        return make_response("f,Tipo de item importado correctamente")