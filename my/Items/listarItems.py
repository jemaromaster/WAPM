from utils import login_required,controlRol
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date
from models.usuarioModelo import Usuario
from models.itemModelo import Item
from models.proyectoModelo import Proyecto
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
    
    def jasonizar(self, listaItems):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
       
        
        
        for f in listaItems:
            #si no se tiene permiso de consultar items, no se devuelve nada en el listar
            if controlRol(str(f.idFase),'item','consulta')==0:
                break
            name=sesion.query(Usuario.username).filter(Usuario.id==f.autorVersion_id).first()
            p=p+json.dumps({"idItem":f.idItem , "nombreItem":f.nombreItem, "version": f.version, "prioridad":f.prioridad, 
                        "fechaInicio": str(f.fechaInicio), "fechaFinalizacion": str(f.fechaFinalizacion), "tipoItem_id": f.tipoItem_id, 
                        "costo": f.costo, "complejidad": f.complejidad, "estado": f.estado, "autorVersion_id":f.autorVersion_id,
                        "nombreAutorVersion": name, "descripcion":f.descripcion, "idFase":f.idFase}, separators=(',',':'))+",";
           
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        


class ListarItems(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idP', '')
        idFase=flask.request.args.get('idF', '')
        
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
        elif(sidx=='version'):
            filtrarPor='version'
        elif(sidx=='costo'):
            filtrarPor='costo'
        elif(sidx=='fechaFinalizacion'):
            filtrarPor='fecha_finalizacion'
        elif(sidx=='fechaInicio'):
            filtrarPor='fecha_inicio'
        elif(sidx=='estado'):
            filtrarPor='estado'
        elif(sidx=='nombreAutorVersion'):
            filtrarPor='autorVersion_id'
             
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        ############33
        
        ###############33
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            nombreItem='%';  
            version='%'; costo='%';
            estado='%'
            autor='%'
            
            for comp in vector:
                if(comp['field']=='nombreItem'):
                    nombreItem=vector[i]['data'].strip() + '%'
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='version':
                    version=vector[i]['data'].strip()
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='costo':
                    costo=vector[i]['data'].strip()
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='estado':
                    estado=vector[i]['data'].strip()
                    i=i+1
                    #field=vector[i]['field']
                    continue
                if comp['field']=='autor':
                    autor=vector[i]['data'].strip()+'%'
                    i=i+1
                    #field=vector[i]['field']
                    continue
            
            #estado=vector[i]['data']
           
            excep=''
            if(estado=='todos'):
               estado='%'
               excep='inactivo'
               
            projectLeaderId=flask.session['idUsuario']
         
            listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.nombreItem.like(nombreItem))\
                                                    .filter(Item.estado.like(estado))\
                                                    .filter(Item.estado!=excep)\
                                                    .filter(Item.idFase==idFase)\
                                                    [desde:hasta]
            
                                                    
                                                    #.filter(Usuario.username.like(autor))
                                                    
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.nombreItem.like(nombreItem))\
                                                    .filter(Item.estado==estado)\
                                                    .filter(Item.idFase==idFase)\
                                                    .count()
            
                
        else:
            #si no hubo filtro entonces se envian los datos de items activos
            
             listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.idFase==idFase).\
                                                    filter(Item.estado!='inactivo')[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
             total=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.idFase==idFase)\
                                                    .filter(Item.estado!='inactivo').count()
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