from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date
from sqlalchemy import or_
from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.itemModelo import Relacion
from models.usuarioModelo import Usuario

sesion=Session()

class ListarItemsRelacionarMiniDialogoComboBox(flask.views.MethodView):
    
    def jasonizar(self, fl):
        """
        modulo que jasoniza la respuesta
        @type fl:Relacion[]
        @param fl: query de las Relaciones 
        """
        cad=''
        pre="["
        #print('fl is'+ str(fl))
        if(fl is not None):
            for f in fl:
                cad=cad+ json.dumps({"idItem":f.idItem , "nombreItem":f.tag}, separators=(',',':'));
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
        else:
            cad=cad+ json.dumps({"idItem":0 , "nombreItem":'ninguno'}, separators=(',',':'));
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self):
        """
        Recibe la peticion de listar relaciones, segun los parametros que incluya la peticion.
        @type idItem: String
        @param idItem: id del item del cual listar los archivos 
        @type idFase: String
        @param idFase: id de la fase
        """ 
        #se obtiene los datos de post del server
        idItem=idTI=flask.request.args.get('idItem', '')
        idFase=flask.request.args.get('idFase', '')
        
        faseMenor=int(idFase)-1;
        relLista=sesion.query(Item).filter(or_(Item.idFase==idFase,Item.idFase==str(faseMenor)))\
                                    .filter(Item.estado!='inactivo').filter(Item.idItem!=idItem)\
                                    .all()
        #or Item.idFase==str(int(idFase)-1)
        
        respuesta=self.jasonizar(relLista)
        sesion.close()
        return respuesta
        