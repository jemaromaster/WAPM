from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.itemModelo import Relacion
from models.usuarioModelo import Usuario

sesion=Session()

class ListarItemsRelacionarMiniDialogoComboBox(flask.views.MethodView):
    
    def jasonizar(self, fl):
        """
        modulo que jasoniza la respuesta
        """
        cad=''
        pre="["
        #print('fl is'+ str(fl))
        if(fl is not None):
            for f in fl:
                cad=cad+ json.dumps({"idItem":f.idItem , "nombreItem":'F'+str(f.idFase)+'.'+f.nombreItem}, separators=(',',':'));
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
        else:
            cad=cad+ json.dumps({"idItem":0 , "nombreItem":'ninguno'}, separators=(',',':'));
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self):
        #se obtiene los datos de post del server
        idItem=idTI=flask.request.args.get('idItem', '')
        idFase=flask.request.args.get('idFase', '')
        relLista=sesion.query(Item).filter(Item.idFase==idFase).filter(Item.estado!='inactivo').all()
        #or Item.idFase==str(int(idFase)-1)
        
        respuesta=self.jasonizar(relLista)
        return respuesta
        