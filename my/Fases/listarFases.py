from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.faseModelo import Fase
from models.proyectoModelo import Proyecto
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    faseas de un proyecto al servidor. Se obtienen de la bd las filas a 
    devolver dentro de la lista y se convierte a un formato
    json para que pueda ser interpretado por el navegador 
    """
    totalPages=1
    currPage=1
    totalRecords=1
    rows=1
    
    def __init__(self, totalPages,currPage,totalRecords,rows):
        """
        Constructor de la clase.
        @type  totalPages: number
        @param totalPages: Indica el numero de paginas que tendra el listado.
        @type  currPage: number
        @param currPage: Indica el numero de pagina actual.
        @type  totalRecords: number
        @param totalRecords: Indica el numero de registros en el listado.
        @type  rows: number
        @param rows: Indica el numero de filas por pagina que se tendra dentro del listado.
        """
        self.totalPages=totalPages
        self.currPage=currPage
        self.totalRecords=totalRecords
        self.rows=rows
    
    def jasonizar(self, listaFase):
        """
        Modulo que jasoniza la respuesta.
        @type  listaFase: Fase[]
        @param listaFase: Resultado de una consulta que trae los datos de las fases a inicluir en el listado
            de fases que se devolvera al cliente.
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for fase in listaFase:
            p=p+"{\"idFase\": \""+str(fase.idFase)+"\",\"nombreFase\": \""+ \
                fase.nombreFase+ \
                "\",\"fechaInicio\": \""+str(fase.fechaInicio)+"\", \"fechaFinalizacion\": \""+ \
                str(fase.fechaFinalizacion) +\
                "\", \"descripcion\": \""+fase.descripcion+"\", \"ordenFase\":\"" + fase.tag+"\", \"estado\":\"" + fase.estado +\
                "\",\"idProyecto\":\"" + str(fase.idProyecto) + "\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarComboFases(flask.views.MethodView):  
    """
    Clase que realiza un listado de fases segun los datos que se 
    reciban del cliente
    """      
    @login_required
    def post(self):
        """
        Recibe la peticion de listar los nombres y ids de fase para su utilizacion en comboBox en el cliente
        @type idProyecto: String
        @param idProyecto: Id del proyecto sobre el cual se filtraran las fases del listado
        """
        idProyecto=flask.request.form['idProyecto']
        print "id proyecto en listar combo fases:  " + idProyecto
        if(idProyecto=='' or idProyecto=='0'):
            sesion.close()
            return "[]"
        
        lf=sesion.query(Fase).order_by("id asc").filter(Fase.idProyecto==int(idProyecto))
        prejsonF='['
        jsonF=''
        for fase in lf:
            jsonF=jsonF+"{\"idFase\":\""+str(fase.idFase)+"\",\"nombreFase\":\""+fase.nombreFase+"\"},"
        jsonF=jsonF[0:len(jsonF)-1]    
        jsonF=prejsonF+jsonF+"]"
        sesion.close()        
        return jsonF
        
        

class ListarFases(flask.views.MethodView):
    """
    Clase que realiza un listado de fases segun los datos que se 
    reciban del cliente
    """
    @login_required
    def get(self):
        """
        Recibe la peticion de listar fases, segun los parametros que incluya la peticion.
        @type page : string
        @param page : parametro que indica el numero de pagina actual.
        @type rows : string
        @param rows : parametro que indica la cantidad de filas por pagina
        @type idProyecto : string
        @param idProyecto : indica sobre que proyecto filtrar las fases
        """ 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyectoPD', '')
        
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='nombreFase'):
            filtrarPor='nombre'
        elif(sidx=='fechaInicio'):
            filtrarPor='fecha_inicio'
        elif(sidx=='fechaFinal'):
            filtrarPor='fecha_finalizacion'
        elif(sidx=='estado'):
            filtrarPor='estado'
        elif(sidx=='ordenFase'):
            filtrarPor='tag'
        
             
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            nombreFase='%';  
            fechaInicio='%'; fechaFinalizacion='%';
            estado='%'
            
            for comp in vector:
                if(comp['field']=='nombreFase'):
                    nombreFase=vector[i]['data'].strip() + '%'
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='estado':
                    estado=vector[i]['data'].strip()+'%'
                    i=i+1
                    #field=vector[i]['field']
                    continue
            
            #estado=vector[i]['data']
            print (nombreFase + estado)
                  
           
            projectLeaderId=flask.session['idUsuario']
         
            listaFase=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==int(idProyecto))\
                                                    .filter(Fase.nombreFase.like(nombreFase))\
                                                    .filter(Fase.estado.like(estado))[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==int(idProyecto))\
                                                    .filter(Fase.nombreFase.like(nombreFase))\
                                                    .filter(Fase.estado.like(estado)).count()
                
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            
            print 'el id proyeceeecto es' + str(idProyecto)
            listaFase=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==int(idProyecto))[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==int(idProyecto)).count()
        print total
        print desde
        print hasta 
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=r.jasonizar(listaFase)
        sesion.close()
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"