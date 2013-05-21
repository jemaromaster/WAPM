from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session

from models.rolProyectoModelo import RolProyecto 
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from models.faseModelo import Fase

sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    roles de proyecto al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaRolEnUsuario,listaRolProyecto,enUsuario):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        SIoNO='No'
        if enUsuario =='Todos':
            for rol in listaRolProyecto:
                if rol in listaRolEnUsuario:
                    SIoNO='Si'
                else:
                    SIoNO='No'
                p=p+"{\"idRol\":\""+str(rol.id)+"\",\"nombre\": \""+rol.nombre+"\",\"descripcion\": \""+rol.descripcion +"\",\"enUsuario\":\""+SIoNO+"\"},"    
        elif enUsuario=='Si':
            SIoNO='Si'
            for rol in listaRolEnUsuario:
                p=p+"{\"idRol\":\""+str(rol.id)+"\",\"nombre\": \""+rol.nombre+"\",\"descripcion\": \""+rol.descripcion +"\",\"enUsuario\":\""+SIoNO+"\"},"
        elif enUsuario=='No':
            SIoNO='No'
            for rol in listaRolProyecto:
                if rol not in listaRolEnUsuario:
                    p=p+"{\"idRol\":\""+str(rol.id)+"\",\"nombre\": \""+rol.nombre+"\",\"descripcion\": \""+rol.descripcion +"\",\"enUsuario\":\""+SIoNO+"\"},"
        
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        
        return p 
        
class ListarRolUsuario(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        idUsuario=flask.request.args.get('idUsuario', '') 
        if(idUsuario == '' or idUsuario == '0'):
            return "Usuario no valido"
        if(idProyecto == '' or idProyecto == '0'):
            return "Proyecto no valido"
        #caluclo de paginacion 
        enUsuario='Todos'
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server
        if(sidx=='nombre'):
            filtrarPor='rol_proyecto.nombre'
        elif(sidx=='descripcion'):
            filtrarPor='rol_proyecto.descripcion'
        
        filtrarPor= "\""+ filtrarPor + '\" ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            cantidad=len(vector)
           
            nombre='%'; descripcion='%'; 
            
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
                if field== 'enUsuario':
                    enUsuario=vector[i]['data']
                    i=i+1
                    continue    
            listaRolProyecto=sesion.query(RolProyecto).join(Fase).join(Proyecto).filter(Proyecto.idProyecto == int(idProyecto)).\
                                                    filter((RolProyecto.nombre.like(nombre )& \
                                                    RolProyecto.descripcion.like(descripcion)))\
                                                    .filter(RolProyecto.estado=="activo")[desde:hasta] 
                                                    
            total==sesion.query(RolProyecto).join(Fase).join(Proyecto).filter(Proyecto.idProyecto == int(idProyecto)).\
                                                    filter((RolProyecto.nombre.like(nombre )& \
                                                    RolProyecto.descripcion.like(descripcion)))\
                                                    .filter(RolProyecto.estado=="activo").count();
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            listaRolProyecto=sesion.query(RolProyecto).join(Fase).join(Proyecto).filter(Proyecto.idProyecto == int(idProyecto))\
                                                    .filter(RolProyecto.estado=="activo")[desde:hasta]
            total=sesion.query(RolProyecto).join(Fase).join(Proyecto).filter(Proyecto.idProyecto == int(idProyecto))\
                                                    .filter(RolProyecto.estado=="activo").count()
        
        listaRolEnUsuario=sesion.query(RolProyecto).join(Fase).join(Proyecto).filter(Proyecto.idProyecto == int(idProyecto)).join(RolProyecto.usuarios).filter(Usuario.id==int(idUsuario))
            
        print total 
        print desde
        print hasta 
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(listaRolEnUsuario,listaRolProyecto,enUsuario)
        sesion.close()
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"