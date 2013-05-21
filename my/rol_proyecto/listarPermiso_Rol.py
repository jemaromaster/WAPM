from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.rolProyectoModelo import RolProyecto 
from models.permisoModelo import Permiso

sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    permisos en un rol al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, todosPermiso, listaPermisoEnRol, enRol):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        SIoNO='no'
        if(enRol=='Todos'):
            for permiso in todosPermiso:
                if permiso in listaPermisoEnRol:
                    SIoNO='Si'
                else:
                    SIoNO='No'
                
                p=p+"{\"nombre\": \""+permiso.nombre+"\",\"descripcion\": \""+permiso.descripcion+"\", \"enRol\": \""+SIoNO+"\",\"idPermiso\": \""+str(permiso.id)+"\"},"
        elif enRol=='Si':
            SIoNO='Si'
            for permiso in listaPermisoEnRol:
                p=p+"{\"nombre\": \""+permiso.nombre+"\",\"descripcion\": \""+permiso.descripcion+"\", \"enRol\": \""+SIoNO+"\",\"idPermiso\": \""+str(permiso.id)+"\"},"
        elif enRol=='No':
            SIoNO='No'
            for permiso in todosPermiso:
                if permiso not in listaPermisoEnRol:
                    p=p+"{\"nombre\": \""+permiso.nombre+"\",\"descripcion\": \""+permiso.descripcion+"\", \"enRol\": \""+SIoNO+"\",\"idPermiso\": \""+str(permiso.id)+"\"},"
        
            
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarPermisosRol(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idRolAFiltrar=flask.request.args.get('idRol', '')
        if idRolAFiltrar =='' or idRolAFiltrar =='0':
            return "NO HAY ID ROL"
        enRol='Todos'
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server
        if(sidx=='nombre'):
            filtrarPor='nombre'
        elif(sidx=='descripcion'):
            filtrarPor='descripcion'
        
        filtrarPor= "\""+ filtrarPor + '\" ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
                
            nombre='%'; descripcion='%'; 
            enRol='%';
            cantidad=len(vector)
            while(i<cantidad):
                field=vector[i]['field']
                if(field=='nombre'):
                    nombre=vector[i]['data'] + '%'
                    i=i+1
                    continue
                if field=='descripcion':
                    descripcion=vector[i]['data']+'%'
                    i=i+1
                    continue
                if field=='enRol':
                    enRol=vector[i]['data']
                    i=i+1
                    continue
            todosPermisos=sesion.query(Permiso).order_by(filtrarPor).filter((Permiso.nombre.like(nombre)& \
                                                    Permiso.descripcion.like(descripcion)))[desde:hasta]  
                                                    
            total=sesion.query(Permiso).order_by(filtrarPor).filter((Permiso.nombre.like(nombre )& \
                                                    Permiso.descripcion.like(descripcion))).count();
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            todosPermisos=sesion.query(Permiso).order_by(filtrarPor).all()[desde:hasta]                                                    
            total=sesion.query(Permiso).order_by(filtrarPor).count()

        listaPermisoEnRol=sesion.query(Permiso).join(RolProyecto.permisos)\
                                    .filter(RolProyecto.id==idRolAFiltrar)
                                    
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
            
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(todosPermisos,listaPermisoEnRol, enRol)
        sesion.close()
        return respuesta    