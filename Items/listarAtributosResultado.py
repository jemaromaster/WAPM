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
    """
    Clase utilizada cuando se hace una peticion de listado de 
    instancias de atributos al servidor
    """
    def format_fecha(self, fecha):
        print("es" + fecha)
        
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    def jasonizar(self, i,version):
        """
        modulo que jasoniza la respuesta
        @type i:AtributosInstancias[]
        @param i: query de los atributos
        @type version: String
        @param version: version del item
        """
        cad=''
        pre="["
        #print('fl is'+ str(fl))
        if(i is not None):
            for s in i:
                #consulta=sesion.query(Atributos).filter(Atributos.nombreAtributo==s[0].nombreCampo).all()
                id=s.tipoPrimario
                
                if(id=='Texto'):
                    aux=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaCadena.version==version).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":aux.cadena}, separators=(',',':'));
                elif(id=='Numerico'):
                    aux=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaNumerico.version==version).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":str(aux.numerico)}, separators=(',',':'));
                elif(id=='Entero'):
                    aux=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaEntero.version==version).first()
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":str(aux.entero)}, separators=(',',':'));
                elif(id=='Fecha'):
                    aux=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                    .filter(InstanciaFecha.version==version).first()
                    fecha_formateada=self.format_fecha(str(aux.fecha))
                    cad=cad+ json.dumps({"nombreInput":s.nombreCampo , "valor":fecha_formateada}, separators=(',',':'));
                    
                cad=cad + ","
            cad=cad[0:len(cad)-1] 
        cad=pre + cad+"]"    
        return cad 
    
    @login_required
    def get(self):
        """
        Recibe la peticion de listar los campos de los atributos dependiendo del tipo de item, segun los parametros que incluya la peticion.
        @type idFase: String
        @param idFase: id de fase de la cual listar los archivos 
        @type idItem: String
        @param idItem: id de item del cual listar los archivos 
        @type idTipoItem: String
        @param idTipoItem: id del tipo de item
        @type version: String
        @param version: version del item 
        """ 
        #se obtiene los datos de post del server
        idFase=flask.request.args.get('idFase', '')
        idTI=flask.request.args.get('idTipoItem', '')
        idItem=flask.request.args.get('idItem', '')
        version=flask.request.args.get('version', '')
        i=sesion.query(InstanciaTipoItem)\
                                .filter(InstanciaTipoItem.idItem==int(idItem)).all();
        for s in i:
            print str(s.idInstanciaTipoItem)+","+str(s.nombreCampo)+","+ str(s.tipoPrimario)
        
        respuesta=self.jasonizar(i,version)
        sesion.close()
        return respuesta
        