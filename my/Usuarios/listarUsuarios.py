from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.usuarioModelo import Usuario 
from models.proyectoModelo import Proyecto
from models.rolSistemaModelo import RolSistema
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    usuario al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaUsuario):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        admin=sesion.query(RolSistema).filter(RolSistema.nombre=="Administrador").one()
        pl=sesion.query(RolSistema).filter(RolSistema.nombre=="Project Leader").one()
        
        for usuario in listaUsuario:
            rolAdmin="0";rolPL="0"
            if admin in usuario.roles_sistema:
                rolAdmin="1"
            if pl in usuario.roles_sistema:
                rolPL="1"
            p=p+"{\"nombreUsuario\": \""+usuario.username+"\",\"nombre\": \""+usuario.nombres+"\", \"idUsuario\": \""+str(usuario.id)+"\",\"email\": \""+usuario.email+"\", \"ci\": \""+usuario.ci +"\", \"apellido\": \""+usuario.apellidos+"\", \"telefono\": \""+usuario.telefono+"\", \"direccion\": \""+usuario.direccion+"\", \"pass\": \""+usuario.passwd+"\", \"pl\": \""+rolPL+"\",\"admin\": \""+rolAdmin+"\",\"observacion\": \""+usuario.observacion+"\", \"activo\":\""+usuario.activo+"\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        
        
        return p 
class ListarComboUsuarios(flask.views.MethodView):
    @login_required
    def post(self):
        idProyecto=flask.request.form['idProyecto']
        listaUsuario=sesion.query(Usuario).join(Proyecto.usuariosMiembros).filter(Proyecto.idProyecto==int(idProyecto))
        pre='['
        p=''
        for usuario in listaUsuario:
            print " el usuario es! " + usuario.username
            p=p+"{\"nombreUsuario\":\""+usuario.username+"\", \"idUsuario\" : \" "+str(usuario.id)+"\"},"
        p=p[0:len(p)-1]
        suf=']'
        respuesta=pre+p+suf
        return respuesta
        
class ListarUsuarios(flask.views.MethodView):
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
        if(sidx=='nombreUsuario'):
            filtrarPor='username'
        elif(sidx=='nombre'):
            filtrarPor='nombres'
        elif(sidx=='apellido'):
            filtrarPor='apellidos'
        elif(sidx=='email'):
            filtrarPor='email'
        elif(sidx=='activo'):
            filtrarPor='activo'
        
        filtrarPor= "\""+ filtrarPor + '\" ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            field=vector[0]['field']
            nombreUsuario='%'; nombre='%'; 
            apellido='%'; email='%';
            direccion='%'
            
            while(field!='activo'):
                if(field=='nombreUsuario'):
                    nombreUsuario=vector[i]['data'] + '%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='nombre':
                    nombre=vector[i]['data']+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='apellido':
                    apellido=vector[i]['data']+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
                if field=='email':
                    email=vector[i]['data']+'%'
                    i=i+1
                    field=vector[i]['field']
                    continue
            
            activo=vector[i]['data']
           
            
            
            listaUsuario=sesion.query(Usuario).order_by(filtrarPor).\
                                                    filter((Usuario.username.like(nombreUsuario )& \
                                                    Usuario.nombres.like(nombre)&  \
                                                    Usuario.apellidos.like(apellido)&  \
                                                    Usuario.direccion.like(direccion)& \
                                                    Usuario.email.like (email) & \
                                                    Usuario.activo.like(activo)))[desde:hasta] 
                                                    
            total=sesion.query(Usuario).filter((Usuario.username.like(nombreUsuario )& \
                                                    Usuario.nombres.like(nombre)&  \
                                                    Usuario.apellidos.like(apellido)&  \
                                                    Usuario.direccion.like(direccion)& \
                                                    Usuario.email.like (email) & \
                                                    Usuario.activo.like(activo))).count();
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            listaUsuario=sesion.query(Usuario).order_by(filtrarPor).filter(\
                                                    Usuario.activo.like('true'))[desde:hasta]
            total=sesion.query(Usuario).filter(Usuario.activo=='true').count()
        print total 
        print desde
        print hasta 
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(listaUsuario)
        sesion.close()
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"