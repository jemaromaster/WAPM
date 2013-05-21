from utils import login_required
import flask.views
from flask import jsonify,json, g, make_response
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.itemModelo import Relacion
from models.usuarioModelo import Usuario

from sqlalchemy import or_

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
    
    def jasonizar(self, listaRel, idItem):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
       
        
        
        for f in listaRel:
            r_descripcion=''
            i=None
            if(f.padre_id==idItem):
                r_descripcion='Hijo'
                id_item_relacionado=f.hijo_id;
                i=sesion.query(Item).filter(Item.idItem==f.hijo_id).first()
            elif(f.hijo_id==idItem):
                r_descripcion='Padre'
                id_item_relacionado=f.padre_id;
                i=sesion.query(Item).filter(Item.idItem==f.padre_id).first()
                
                
            if(i is None):
                    return make_response ('t,No existe item con ese id')    
            p=p+json.dumps({"idRelacion": f.idRelacion,"relacion":r_descripcion , "idItemRelacionado":id_item_relacionado,  \
                            "nombreItem": i.tag , "estado": i.estado}, separators=(',',':'))+",";
           
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        


class ListarRelaciones(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idP', '')
        idFase=flask.request.args.get('idF', '')
        idItem=flask.request.args.get('idIt', '')
        
        print "ide del item es :  "+ idItem
        if idItem is not None and idItem!='':
            idItem=int(idItem)
        else:
            idItem=0
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='relacion'):
            filtrarPor='relacion'
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
            
            '''listaItem=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.idFase==idFase).\
                                                    filter(Item.estado!='inactivo')[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(Item).order_by(filtrarPor)\
                                                    .filter(Item.idFase==idFase)\
                                                    .filter(Item.estado!='inactivo').count()'''
            print (filtrarPor);
            listaRel=sesion.query(Relacion).order_by(filtrarPor)\
                                                    .filter(or_(Relacion.hijo_id==idItem, Relacion.padre_id==idItem)).all()
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
        
        respuesta=r.jasonizar(listaRel, idItem)
        sesion.close()
        return respuesta
        
        