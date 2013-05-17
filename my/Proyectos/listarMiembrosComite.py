from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.usuarioModelo import Usuario 
from models.proyectoModelo import Proyecto

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
    
    def jasonizar(self,listaUsuariosEnProyecto,idProyecto,filtroComite):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        proyecto = sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).first()
        enComite=''
        for usuario in listaUsuariosEnProyecto:
            if proyecto in usuario.proyectosComite:
                enComite='si'
            else:
                enComite='no'
                
            if filtroComite == "si" and enComite=="si":    
                p=p+"{\"nombreUsuario\": \""+usuario.username+"\",\"nombre\": \""+usuario.nombres+"\", \"idUsuario\": \""+str(usuario.id)+"\",\"email\": \""+usuario.email+"\", \"ci\": \""+usuario.ci +"\", \"apellido\": \""+usuario.apellidos+"\", \"telefono\": \""+usuario.telefono+"\", \"direccion\": \""+usuario.direccion+"\", \"pass\": \""+usuario.passwd+"\", \"observacion\": \""+usuario.observacion+"\", \"enComite\": \""+ enComite + "\",\"activo\":\""+usuario.activo+"\"},"
            if filtroComite == "no" and enComite=="no":
                p=p+"{\"nombreUsuario\": \""+usuario.username+"\",\"nombre\": \""+usuario.nombres+"\", \"idUsuario\": \""+str(usuario.id)+"\",\"email\": \""+usuario.email+"\", \"ci\": \""+usuario.ci +"\", \"apellido\": \""+usuario.apellidos+"\", \"telefono\": \""+usuario.telefono+"\", \"direccion\": \""+usuario.direccion+"\", \"pass\": \""+usuario.passwd+"\", \"observacion\": \""+usuario.observacion+"\", \"enComite\": \""+ enComite + "\",\"activo\":\""+usuario.activo+"\"},"
            if filtroComite == "todos":
                p=p+"{\"nombreUsuario\": \""+usuario.username+"\",\"nombre\": \""+usuario.nombres+"\", \"idUsuario\": \""+str(usuario.id)+"\",\"email\": \""+usuario.email+"\", \"ci\": \""+usuario.ci +"\", \"apellido\": \""+usuario.apellidos+"\", \"telefono\": \""+usuario.telefono+"\", \"direccion\": \""+usuario.direccion+"\", \"pass\": \""+usuario.passwd+"\", \"observacion\": \""+usuario.observacion+"\", \"enComite\": \""+ enComite + "\",\"activo\":\""+usuario.activo+"\"},"
                    
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarMiembrosComite(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        if idProyecto =='' or idProyecto =='0':
            return "NO HAY ID PROYECTO"
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        enComite='todos'
        
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
        elif(sidx=='enComite'):
            filtrarPor='enComite'
        
        filtrarPor= "\""+ filtrarPor + '\" ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            cantidad=len(vector)
            i=0
            nombreUsuario='%'; nombre='%'; 
            apellido='%'; email='%';
            direccion='%'; 
            
            while(i<cantidad):
                field=vector[i]['field']
                if(field=='nombreUsuario'):
                    nombreUsuario=vector[i]['data'] + '%'
                    i=i+1
                    continue
                if field=='nombre':
                    nombre=vector[i]['data']+'%'
                    i=i+1
                    continue
                if field=='apellido':
                    apellido=vector[i]['data']+'%'
                    i=i+1
                    continue
                if field=='email':
                    email=vector[i]['data']+'%'
                    i=i+1
                    continue
                if field=='enComite':
                    auxEnComite=vector[i]['data']
                    if auxEnComite != "todos":
                        enComite=auxEnComite
                    i=i+1
                    continue
                    
            listaUsuarioEnProyecto=sesion.query(Usuario).join(Proyecto.usuariosMiembros)\
                                    .filter(Proyecto.idProyecto==idProyecto) \
                                    .filter(Usuario.activo=="true")\
                                    .filter(Usuario.username.like(nombreUsuario)&\
                                    Usuario.nombres.like(nombre) & Usuario.apellidos.like(apellido) &\
                                    Usuario.email.like(email))         
            total=sesion.query(Usuario).join(Proyecto.usuariosMiembros)\
                                    .filter(Proyecto.idProyecto==idProyecto) \
                                    .filter(Usuario.activo=="true")\
                                    .filter(Usuario.username.like(nombreUsuario)&\
                                    Usuario.nombres.like(nombre) & Usuario.apellidos.like(apellido) &\
                                    Usuario.email.like(email)).count()                        
                        
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            listaUsuarioEnProyecto=sesion.query(Usuario).join(Proyecto.usuariosMiembros)\
                                    .filter(Proyecto.idProyecto==idProyecto)\
                                    .filter(Usuario.activo=="true")
            total=sesion.query(Usuario).join(Proyecto.usuariosMiembros)\
                                    .filter(Proyecto.idProyecto==idProyecto)\
                                    .filter(Usuario.activo=="true").count()
           
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
            
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(listaUsuarioEnProyecto,idProyecto,enComite)
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"