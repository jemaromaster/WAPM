from utils import login_required,miembroComite_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto
from models.solicitudCambioModelo import SolicitudCambio
from models.solicitudCambioModelo import Voto
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    solicitud de cambios al servidor. Se obtienen de la bd las filas a 
    devolver dentro de la lista y se convierte a un formato
    json para que pueda ser interpretado por el navegador 
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
    
    def jasonizar(self, listaVotos):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for voto in listaVotos:
            p=p+"{\"miembro\": \""+voto.username+"\",\"voto\": \""+ \
                voto.voto+"\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarVotos(flask.views.MethodView):
    
    @login_required
    @miembroComite_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idSC=flask.request.args.get('idSC', '')
        
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='miembro'):
            filtrarPor='username'
        elif(sidx=='voto'):
            filtrarPor='voto'
             
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            miembro='%'
            
            
            for comp in vector:
                if(comp['field']=='miembro'):
                    miembro=comp['data'].strip() + '%'
                    continue
                    
                
            queryVotos=sesion.query(Usuario.username,Voto.voto).order_by(filtrarPor)\
                                                    .filter(Voto.solicitud==int(idSC))\
                                                    .filter(Voto.votante==Usuario.id)
            queryVotos=queryVotos.filter(Usuario.username.like(miembro) )                                        
            total=queryVotos.count()
            listaVotos=queryVotos[desde:hasta]
            
        else:
            queryVotos=sesion.query(Usuario.username,Voto.voto).order_by(filtrarPor)\
                                                    .filter(Voto.solicitud==int(idSC))\
                                                    .filter(Voto.votante==Usuario.id)
            '''
            queryVotos=sesion.query(Usuario.username,Voto.voto).order_by(filtrarPor)\
                                                    .filter(Voto.solicitud==int(idSC))\
                                                    .filter(Voto.votante==Usuario.id)
            '''
            total=queryVotos.count()
            listaVotos=queryVotos[desde:hasta]
            
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=r.jasonizar(listaVotos)
        sesion.close()
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"