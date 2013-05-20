from utils import login_required
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem

sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de \
    tipos de item al servidor. \Se obtienen de la bd las filas a \
    devolver dentro de la lista y se convierte a un formato\
    json para que pueda ser interpretado por el navegador \
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
    
   
    
    def jasonizar(self, listaTipoItem):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
               
        for tipoItem in listaTipoItem:
            p=p+"{\"idTipoItem\": \""+str(tipoItem.idTipoItem)+"\",\"nombreTipoItem\": \""+ \
                tipoItem.nombreTipoItem+ \
                "\",\"estado\": \""+str(tipoItem.estado)+"\", \"descripcion\": \""+ \
                tipoItem.descripcion + "\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarTipoItem(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        
        '''if( idFase== '' ):
            return "Error, no se ha proporcionado idFase"'''
        if(search=='true'):
            idFase=flask.session['idFaseActualTipoItem']
        else:
            idFase=flask.request.args.get('idFase', '')
            flask.session['idFaseActualTipoItem']=idFase
            
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        filtrarPor='estado'
        if(sidx=='nombreTipoItem'):
            filtrarPor='nombre'
        elif(sidx=='descripcion'):
            filtrarPor='descripcion'
        elif(sidx=='estado'):
            filtrarPor='estado'
        
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        print filtrarPor
        if (search=='true'):
            
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            cantidad=len(vector)
            
            nombreTipoItem='%'
            descripcion='%'
            estado='%'
            
            while(i<cantidad):
                field=vector[i]['field']
                if(field=='nombreTipoItem'):
                    nombreTipoItem=vector[i]['data'].strip() + '%'
                    i=i+1
                    continue
               
                if field=='descripcion':
                    descripcion=vector[i]['data'].strip()+'%'
                    i=i+1
                    continue
                if field=='estado':
                    elEstado=vector[i]['data'].strip()
                    if elEstado!="todos":
                        estado=elEstado+'%'
                    i=i+1
                    continue

            projectLeaderId=flask.session['idUsuario']
            listaTipoItem=sesion.query(TipoItem).order_by(filtrarPor)\
                                                    .filter(TipoItem.fase_id==idFase)\
                                                    .filter(TipoItem.nombreTipoItem.like(nombreTipoItem) &\
                                                           TipoItem.descripcion.like(descripcion)&\
                                                    TipoItem.estado.like(estado))[desde:hasta]
           
            total=sesion.query(TipoItem).order_by(filtrarPor)\
                                                    .filter(TipoItem.fase_id==int(idFase))\
                                                    .filter(TipoItem.nombreTipoItem.like(nombreTipoItem) &\
                                                           TipoItem.descripcion.like(descripcion)&\
                                                    TipoItem.estado.like(estado)).count()
            
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            
            #print 'el id proyeceeecto es' + str(idProyecto)
            listaTipoItem=sesion.query(TipoItem).order_by(filtrarPor)\
                                                    .filter((TipoItem.fase_id)==(idFase))[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(TipoItem).order_by(filtrarPor)\
                                                    .filter(TipoItem.fase_id==int(idFase)).count()
        """print total
        print desde
        print hasta """
        resto=total%rows
        if resto == 0:
            totalPages=total/rows
        else:
            totalPages=total/rows +1
        r=Respuesta(totalPages,page,total,rows);
        
        # elUser=sesion.query(Usuario).filter(Usuario.id==projectLeaderId).first()
        
        respuesta=r.jasonizar(listaTipoItem)
        return respuesta
       
   