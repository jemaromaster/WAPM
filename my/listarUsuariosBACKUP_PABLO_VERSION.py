from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.usuarioModelo import Usuario 
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
        
        #hasta=self.currPage*self.rows
        #desde=hasta-self.rows
        #listaUsuario= listaUsuario [desde:hasta]
        
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        for usuario in listaUsuario:
            p=p+"{\"nombreUsuario\": \""+usuario.username+"\",\"nombre\": \""+usuario.nombres+"\", \"idUsuario\": \""+str(usuario.id)+"\",\"email\": \""+usuario.email+"\", \"ci\": \""+usuario.ci +"\", \"apellido\": \""+usuario.apellidos+"\", \"telefono\": \""+usuario.telefono+"\", \"direccion\": \""+usuario.direccion+"\", \"pass\": \""+usuario.passwd+"\", \"observacion\": \""+usuario.observacion+"\", \"activo\":\""+usuario.activo+"\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarUsuarios(flask.views.MethodView):
    @login_required
    def get(self): 
        total=sesion.query(Usuario).count()
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        page=long(param1)
        rows=long(param2)
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            sidx=flask.request.args.get('sidx', '')
            sord=flask.request.args.get('sord', '')
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
            
            activo=vector[i]['field']
            #if (obj.rules[0].field=="nombreUsuario"):
            #print(obj.rules[0].field)listaUsuario=sesion.query(Usuario).all()
            #aca tiene que la parte de filtrado
            #listaUsuario=sesion.query(Usuario).filter(Usuario.username==nombreUsuario).all()
            #listaUsuario=sesion.query(Usuario).filter(Usuario.username).all()
            listaUsuario=sesion.query(Usuario).filter((Usuario.username.like(nombreUsuario )& \
                                                    Usuario.nombres.like(nombre)&  \
                                                    Usuario.apellidos.like(apellido)&  \
                                                    Usuario.direccion.like(direccion)& \
                                                    Usuario.email.like (email))) \
                                                    .slice((page*rows),(page*rows)+rows)
        else:
            listaUsuario=sesion.query(Usuario).all().slice((page*rows),(page*rows)+rows)
        #total=listaUsuario=sesion.query(Usuario).count()
        total=0
        for filas in listaUsuario: 
            total=total+1
        print total  
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(listaUsuario)
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"