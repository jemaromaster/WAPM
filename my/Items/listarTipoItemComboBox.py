from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem

sesion=Session()

class ListarTipoItemComboBox(flask.views.MethodView):
    
    def jasonizar(self, fl):
        """
        modulo que jasoniza la respuesta
        """
        cad=''
        pre="["
        #print('fl is'+ str(fl))
        if(fl is not None):
            for f in fl:
                cad=cad+ json.dumps({"idTipoItem":f.idTipoItem , "nombreTipoItem":f.nombreTipoItem}, separators=(',',':'));
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
        else:
            cad=cad+ json.dumps({"idTipoItem":0 , "nombreItem":'ninguno'}, separators=(',',':'));
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self):
        #se obtiene los datos de post del server
        idTI=flask.request.args.get('idFase', '')
        tipoItemLista=sesion.query(TipoItem).filter(TipoItem.fase_id==idTI)
       
        respuesta=self.jasonizar(tipoItemLista)
        return respuesta
        