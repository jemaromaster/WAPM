from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.atributosModelo import Atributos
from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.instanciaAtributos import InstanciaTipoItem, InstanciaNumerico, InstanciaFecha, InstanciaEntero, InstanciaCadena

sesion=Session()

class ListarAtributosResultado(flask.views.MethodView):
    
    def format_fecha(self, fecha):
        print("es" + fecha)
        
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    def jasonizar(self, i):
        """
        modulo que jasoniza la respuesta
        """
        cad=''
        pre="["
        #print('fl is'+ str(fl))
        if(i is not None):
            for s in i:
                #consulta=sesion.query(Atributos).filter(Atributos.nombreAtributo==s[0].nombreCampo).all()
                id=s.tipoPrimario
                
                if(id=='Texto'):
                    aux=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==int(s.idInstanciaTipoItem)).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":aux.cadena}, separators=(',',':'));
                elif(id=='Numerico'):
                    aux=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==int(s.idInstanciaTipoItem)).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":aux.numerico}, separators=(',',':'));
                elif(id=='Entero'):
                    aux=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==int(s.idInstanciaTipoItem)).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":aux.entero}, separators=(',',':'));
                elif(id=='Fecha'):
                    aux=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==int(s.idInstanciaTipoItem)).first()
                    
                    fecha_formateada=self.format_fecha(str(aux.fecha))
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":fecha_formateada}, separators=(',',':'));
                    
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self):
        #se obtiene los datos de post del server
        idFase=flask.request.args.get('idFase', '')
        idTI=flask.request.args.get('idTipoItem', '')
        idItem=flask.request.args.get('idItem', '')
        i=sesion.query(InstanciaTipoItem)\
                                .filter(InstanciaTipoItem.idItem==idItem).all();
        for s in i:
            print str(s.idInstanciaTipoItem)+","+str(s.nombreCampo)+","+ str(s.tipoPrimario)
        
        respuesta=self.jasonizar(i)
        return respuesta
        