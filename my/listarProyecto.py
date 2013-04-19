from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    proyectos al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaProyecto, nombreProjectLeader):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for proy in listaProyecto:
            p=p+"{\"idProyecto\": \""+str(proy.idProyecto)+"\",\"nombreProyecto\": \""+ \
                proy.nombreProyecto+"\", \"idProjectLeader\": \""+str(proy.projectLeaderId)+ \
                "\",\"fechaInicio\": \""+str(proy.fechaInicio)+"\", \"fechaFinalizacion\": \""+ \
                str(proy.fechaFinalizacion) +"\", \"presupuesto\": \""+str(int(proy.presupuesto))+ \
                "\", \"observacion\": \""+proy.observacion+"\", \"nroFases\": \""+ \
                str(proy.nroFases)+"\", \"estado\":\"" + proy.estado +\
                "\",\"nombreProjectLeader\":\"" + nombreProjectLeader + "\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarProyectos(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server
        if(sidx=='nombreProyecto'):
            filtrarPor='nombre_proyecto'
        elif(sidx=='fechaInicio'):
            filtrarPor='fecha_inicio'
        elif(sidx=='fechaFinal'):
            filtrarPor='fecha_final'
        elif(sidx=='presupuesto'):
            filtrarPor='presupuesto'
        elif(sidx=='estado'):
            filtrarPor='activo'
        
        
        projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        print filtrarPor
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            field=vector[0]['field']
            nombreProyecto='%'; fechaInicio='%'; 
            fechaFinalizacion='%'; presupuesto='%';
            estado='%'
            
            while(field!='estado'):
                if(field=='nombreProyecto'):
                    nombreProyecto=vector[i]['data'].strip() + '%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='fechaInicio':
                    fechaInicio=vector[i]['data'].strip()+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='fechaFinalizacion':
                    fechaFinalizacion=vector[i]['data'].strip()+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='presupuesto':
                    presupuesto=vector[i]['data'].strip()+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
            
            estado=vector[i]['data']
            
                  
           
            projectLeaderId=flask.session['idUsuario']
            listaUsuario=sesion.query(Proyecto).order_by(filtrarPor).\
                                                    filter(Proyecto.nombreProyecto.like(nombreProyecto) \
                                                    #Proyecto.fechaInicio==date('2013-04-15') &  \
                                                    #Proyecto.fechaFinalizacion.like(fechaFinalizacion)& \
                                                    #Proyecto.presupuesto.like (presupuesto) & \
                                                    #Proyecto.estado.like(estado)) \
                                                    #Proyecto.fechaInicio.like('2013-04-15'))
                                                    ).filter(Proyecto.estado==estado)\
                                                    .filter(Proyecto.projectLeaderId==projectLeaderId)[desde:hasta] 
                                                    #Proyecto.projectLeaderId.like(projectLeaderId)&  \
            total=sesion.query(Proyecto).filter(Proyecto.nombreProyecto.like(nombreProyecto) \
                                                    
                                                    #Proyecto.projectLeaderId.like(projectLeaderId)&  \
                                                    #Proyecto.fechaInicio.like(fechaInicio)&  \
                                                    #Proyecto.fechaFinalizacion.like(fechaFinalizacion)& \
                                                    #Proyecto.presupuesto.like (presupuesto) & \
                                                    ).filter(Proyecto.estado==estado)\
                                                    .filter(Proyecto.projectLeaderId==projectLeaderId)\
                                                    .count();
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            listaUsuario=sesion.query(Proyecto).order_by(filtrarPor)\
                                                    .filter(Proyecto.estado=='activo') \
                                                    .filter(Proyecto.projectLeaderId==projectLeaderId)[desde:hasta]
            total=sesion.query(Proyecto).filter(Proyecto.estado=='activo')\
                                        .filter(Proyecto.projectLeaderId==projectLeaderId).count()
        print total
        print desde
        print hasta 
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        
        elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=r.jasonizar(listaUsuario, elUser.username)
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"