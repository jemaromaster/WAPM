from utils import login_required,controlRol
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.lineaBaseModelo import LineaBase 
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    linea base al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaLB):
        """
        Modulo que jasoniza la respuesta.
        @type  listaLB: LineaBase[]
        @param listaLB: Resultado de una consulta que trae los datos de las Lineas bases a inicluir en el listado
            de lineas bases que se devolvera al cliente.
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        for lb in listaLB:
            if controlRol(str(lb.idFase),'lb','consulta')==0:
                break

            p=p+"{\"idLB\":\""+str(lb.id)+"\",\"descripcion\": \""+lb.descripcion +"\",\"estado\": \""+lb.estado+"\"},"
            # {"nombre":"nombre","idRol":"rol","descripcion":"descripciones"},
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        
        return p 
        
class ListarLB(flask.views.MethodView):
    """
    Clase que realiza un listado de lineas bases segun los datos que se 
    reciban del cliente. Este listado incluye a las lineas bases que 
    se crearon dentro de la fase de un proyecto.
    """     
    @login_required
    def get(self): 
        """
        Recibe la peticion de listar items, segun los parametros que incluya la peticion.
        type page : string
        @param page : parametro que indica el numero de pagina actual.
        @type rows : string
        @param rows : parametro que indica la cantidad de filas por pagina
        @type idFase : string
        @param idFase : indica la fase a la que pertenecen las lineas bases a listar
        """
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idFase=flask.request.args.get('idFase', '') 
        if(idFase == ''):
            return "fase no valida"
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server
        if sidx=='descripcion':
            filtrarPor='descripcion'
        elif(sidx=='estado'):
            filtrarPor='estado'
        
        filtrarPor= "\""+ filtrarPor + '\" ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            cantidad=len(vector)
           
            descripcion='%'; 
            estado='%'
            while(i<cantidad):
                field=vector[i]['field']
                if field=='descripcion':
                    descripcion=vector[i]['data']+'%'
                    i=i+1
                    continue
                if field =='estado':
                    elEstado=vector[i]['data']
                    print "el estado:   " + elEstado
                    if elEstado != "todos":
                        estado=elEstado+'%'
                    i=i+1
                    continue
                
            
            listaLB=sesion.query(LineaBase).order_by(filtrarPor).\
                                                    filter(LineaBase.descripcion.like(descripcion)&\
                                                    LineaBase.estado.like(estado)) \
                                                    .filter(LineaBase.idFase==int(idFase)) [desde:hasta] 
                                                    
            total=sesion.query(LineaBase).order_by(filtrarPor).\
                                                    filter(LineaBase.descripcion.like(descripcion)&\
                                                    LineaBase.estado.like(estado)) \
                                                    .filter(LineaBase.idFase==int(idFase)).count()
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            listaLB=sesion.query(LineaBase).order_by(filtrarPor).filter(LineaBase.idFase==int(idFase))[desde:hasta]
            total=sesion.query(LineaBase).order_by(filtrarPor).filter(LineaBase.idFase==int(idFase)).count()
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        respuesta=r.jasonizar(listaLB)
        sesion.close()
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"