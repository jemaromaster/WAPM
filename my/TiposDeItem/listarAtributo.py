from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.atributosModelo import Atributos

sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de \
    listado de Atributos correspondientes a un Tipo de Item. \Se obtienen de la bd las filas a \
    devolver dentro de la lista y se convierte a un formato
    json para que pueda ser interpretado por el javascript
    """
    totalPages=1
    currPage=1
    totalRecords=1
    rows=1
    
    def __init__(self, totalPages,currPage,totalRecords,rows):
        self.totalPages=totalPages
        self.currPage=currPage
        self.totalRecords=totalRecords
        self.rows=rows
    
    
    def jasonizar(self, listaTipoItem):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
               
        for tipoItem in listaTipoItem:
            p=p+"{\"idTipoItem\": \""+str(tipoItem.idTipoItem)+"\",\"nombreTipoItem\": \""+ \
                tipoItem.nombreTipoItem+ \
                "\",\"estado\": \""+str(tipoItem.estado)+"\", \"descripcion\": \""+ \
                tipoItem.descripcion +\
                "\", \"atributos\":" + self.jsonizarListaAtributos(tipoItem.atributosItem)+ "},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarAtributo(flask.views.MethodView):
    """Clase utilizada para listar todos los atributos correspondiente a un tipo de item determinado"""
    def jsonizarListaAtributos (self, listaAtributos):
        
        
        cad=""
        for atrib in listaAtributos:
            cad=cad+json.dumps({"idAtributos": atrib.idAtributo, "nombreAtributo": atrib.nombreAtributo, "tipoPrimario": atrib.tipoPrimario.nombre,\
                        "longitudCadena":atrib.longitudCadena}, separators=(',',':'))
            cad=cad + ","
        resp="[" + cad[0:len(cad)-1]+"]"
       
        #print resp
        return resp
    
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        idFase=flask.request.args.get('idFase', '')
        idTipoItem=flask.request.args.get('idTipoItem', '')
       
        listaAtributo=sesion.query(Atributos).filter(Atributos.tipoItemId==int(idTipoItem)).all()
                                                #.filter(Proyecto.projectLeaderId==projectLeaderId)
        #total=sesion.query(Atributos).filter(Atributos.tipoItemId==int(idTipoItem)).count()
        
        
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=self.jsonizarListaAtributos(listaAtributo)
        return respuesta
       
   