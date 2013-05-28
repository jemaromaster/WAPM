from utils import login_required,miembroComite_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto
from models.solicitudCambioModelo import SolicitudCambio
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    solicitud de votantes. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaSC):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for sc in listaSC:
            p=p+"{\"idSC\": \""+str(sc.id)+"\",\"descripcion\": \""+ \
                sc.descripcion+ \
                "\", \"estado\":\"" + sc.estado +"\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarSCVotante(flask.views.MethodView):
    
    @login_required
    @miembroComite_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        idUsuario=flask.request.args.get('idUsuario', '')
        
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='descripcion'):
            filtrarPor='descripcion'
        elif(sidx=='estado'):
            filtrarPor='estado'
        elif(sidx=='idSC'):
            filtrarPor='id'
             
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        estado='pendiente'
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            descripcion='%'
            
            
            for comp in vector:
                if(comp['field']=='descripcion'):
                    descripcion=comp['data'].strip() + '%'
                    continue
                if comp['field']=='estado':
                    estado=comp['data'].strip()+'%'
                    continue
                    
                
            querySC=sesion.query(SolicitudCambio).order_by(filtrarPor)\
                                                    .filter(SolicitudCambio.idProyecto==int(idProyecto))\
                                                    .filter(SolicitudCambio.descripcion.like(descripcion) &\
                                                    SolicitudCambio.estado.like(estado))
            listaSC=querySC[desde:hasta]
            total=querySC.count()
            
        else:
            
            querySC=sesion.query(SolicitudCambio).order_by(filtrarPor)\
                                                    .filter(SolicitudCambio.idProyecto==int(idProyecto))\
                                                    .filter(SolicitudCambio.estado.like(estado))
            listaSC=querySC[desde:hasta]
            total=querySC.count()
            
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=r.jasonizar(listaSC)
        sesion.close()
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"