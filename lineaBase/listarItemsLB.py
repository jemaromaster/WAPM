from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.itemModelo import Item
from models.faseModelo import Fase
from models.lineaBaseModelo import LineaBase
from models.solicitudCambioModelo import SolicitudCambio
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    items que pueden ser agregados a una lb. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaItems):
        """
        Modulo que jasoniza la respuesta.
        @type  listaItems: Item[]
        @param listaItems: Resultado de una consulta que trae los datos de los items a inicluir en el listado
            de items que se devolvera al cliente.
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + "\",\"invdata\" : [" 

        for f in listaItems:
            
            p=p+json.dumps({"idItem":f.idItem , "nombreItem":f.nombreItem,
                        "fechaInicio": str(f.fechaInicio), "fechaFinalizacion": str(f.fechaFinalizacion),  
                        "costo": f.costo}, separators=(',',':'))+",";
           
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        


class ListarItemBase(flask.views.MethodView):
    """
    Clase que realiza un listado de items segun los datos que se 
    reciban del cliente. Este listado incluye a los items que pueden
    ser  agregados a una linea base.
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
        @param idFase : id de la fase a la que pertenecen los items a listar
        @type idLB : string
        @param idLB : id de la linea base a la que pertenecn los items a listar
        """
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        
        idFase=0
        if 'idFase' in flask.request.args:
            idFase=flask.request.args.get('idFase', '')
        
        idLB=0
        if 'idLB' in flask.request.args:
            idLB=flask.request.args.get('idLB', '')
            
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='nombreItem'):
            filtrarPor='nombre'
        elif(sidx=='costo'):
            filtrarPor='costo'
        elif(sidx=='fechaFinalizacion'):
            filtrarPor='fecha_finalizacion'
        elif(sidx=='fechaInicio'):
            filtrarPor='fecha_inicio'
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        ############No se deben listar los items que ya se encuentran en una SC
        
        itemtAlreadySC=sesion.query(Item.idItem).filter(SolicitudCambio.estado=="pendiente").join(SolicitudCambio.items).all()
        
        ###############33
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            nombreItem='%';  
            costo='%';
            
            for comp in vector:
                if(comp['field']=='nombreItem'):
                    nombreItem=vector[i]['data'].strip() + '%'
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='costo':
                    costo=vector[i]['data'].strip()
                    i=i+1
                    #field=vector[i]['field']
                    continue
                
            if idLB!=0:
                listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.nombreItem.like(nombreItem))\
                                                        .join(Item.lb).filter(LineaBase.id==idLB)\
                                                        [desde:hasta]
                
                                                        
                                                        #.filter(Usuario.username.like(autor))
                                                        
                                                        #.filter(Proyecto.projectLeaderId==projectLeaderId)
                total=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.nombreItem.like(nombreItem))\
                                                        .join(Item.lb).filter(LineaBase.id==idLB)\
                                                        .count()
            
            else:
                listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.nombreItem.like(nombreItem))\
                                                        .filter(Item.estado.like("aprobado"))\
                                                        .filter(Item.idFase==idFase,\
                                                        ~Item.idItem.in_(itemtAlreadySC))[desde:hasta]
                
                                                        
                                                        #.filter(Usuario.username.like(autor))
                                                        
                                                        #.filter(Proyecto.projectLeaderId==projectLeaderId)
                total=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.nombreItem.like(nombreItem))\
                                                        .filter(Item.estado.like("aprobado"))\
                                                        .filter(Item.idFase==idFase,\
                                                        ~Item.idItem.in_(itemtAlreadySC)).count()
            
                
        else:
            if idLB!=0:
                listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                        .join(Item.lb).filter(LineaBase.id==idLB)\
                                                        [desde:hasta]
                total=sesion.query(Item).order_by(filtrarPor)\
                                                        .join(Item.lb).filter(LineaBase.id==idLB)\
                                                        .count()
            
            else:
                listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.idFase==idFase)\
                                                        .filter(Item.estado=='aprobado',\
                                                        ~Item.idItem.in_(itemtAlreadySC))[desde:hasta]
                                                        #.filter(Proyecto.projectLeaderId==projectLeaderId)
                total=sesion.query(Item).order_by(filtrarPor)\
                                                        .filter(Item.idFase==idFase)\
                                                        .filter(Item.estado=='aprobado',\
                                                        ~Item.idItem.in_(itemtAlreadySC)).count()
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
        
        respuesta=r.jasonizar(listaItem)
        sesion.close()
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"