from utils import login_required,controlRol
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto
from models.itemModelo import Item
from models.faseModelo import Fase
from models.solicitudCambioModelo import SolicitudCambio
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    solicitud de cambios al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaItemAprobar):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for item in listaItemAprobar:
            if controlRol(str(item.idFase),'item','administrar')==1:
                p=p+"{\"idItem\": \""+str(item.idItem)+ \
                    "\",\"idFase\": \""+ item.tag+ \
                    "\", \"estado\":\"" + item.estado + \
                    "\", \"nombreItem\":\"" + item.nombreItem + \
                    "\", \"incluir\":\"" + "no" +"\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarItemAgregar(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        idUsuario=flask.request.args.get('idUsuario', '')
        
        #caluclo de paginacion 
        page=long(param1)
        rows=long(param2)
        
        hasta=page*rows
        desde=hasta-rows
        total=0
        
        sidx=flask.request.args.get('sidx', '')
        sord=flask.request.args.get('sord', '')
        
        
        #se establece el campo de filtro proveniente del server para hacer coincidir con el nombre de la tabla
        if(sidx=='idFase'):
            filtrarPor='idFase'
        elif(sidx=='nombreItem'):
            filtrarPor='nombreItem'
        elif(sidx=='estado'):
            filtrarPor='estado'
        else:
            filtrarPor='idFase'
             
        #se extrae el id de la session cookie
        #projectLeaderId=flask.session['idUsuario']
        
        filtrarPor= filtrarPor + ' ' + sord #establece el si filtrar por asc o desc 
        
        if (search=='true'):
            filters=flask.request.args.get('filters', '')
            obj = json.loads(filters)
            vector=obj['rules']
            i=0
            #field=vector[0]['field']
            idFase='%'
            nombreItem='%'
            
            for comp in vector:
                if(comp['field']=='idFase'):
                    idFase=comp['data'].strip() + '%'
                    continue
                if comp['field']=='nombreItem':
                    nombreItem=comp['data'].strip()+'%'
                    continue
            '''    
            queryItemAgregar=sesion.query(Item.idItem,Item.nombreItem,Item.estado,Fase.tag).filter(Fase.idProyecto==idProyecto,Item.idFase==Fase.idFase,\
                                                            Item.estado.in_(['aprobado', 'bloqueado']));
            queryItemAgregar=queryItemAgregar.filter(Fase.tag.like(idFase),Item.nombreItem.like(nombreItem))
            
            listaItemAgregar=queryItemAgregar[desde:hasta]
            total=queryItemAgregar.count()
            '''
            #controlar que no se encuentre en otra solicitud de cambio pendiente
            
            itemtAlreadySC=sesion.query(Item.idItem).filter(SolicitudCambio.estado=="pendiente").join(SolicitudCambio.items).all()
            
            queryItemAgregar=sesion.query(Item.idItem,Item.nombreItem,Item.estado,Fase.tag,Fase.idFase).filter(Fase.idProyecto==idProyecto,\
                                                            Item.idFase==Fase.idFase,\
                                                            Item.estado.in_(['aprobado', 'bloqueado']),\
                                                            ~Item.idItem.in_(itemtAlreadySC));
            
            queryItemAgregar=queryItemAgregar.filter(Fase.tag.like(idFase),Item.nombreItem.like(nombreItem))
            listaItemAgregar=queryItemAgregar[desde:hasta]
            total=queryItemAgregar.count()
                
            
        else:
            itemtAlreadySC=sesion.query(Item.idItem).filter(SolicitudCambio.estado=="pendiente").join(SolicitudCambio.items).all()
            
            queryItemAgregar=sesion.query(Item.idItem,Item.nombreItem,Item.estado,Fase.tag,Fase.idFase).filter(Fase.idProyecto==idProyecto,\
                                                            Item.idFase==Fase.idFase,\
                                                            Item.estado.in_(['aprobado', 'bloqueado']),\
                                                            ~Item.idItem.in_(itemtAlreadySC));
            listaItemAgregar=queryItemAgregar[desde:hasta]
            total=queryItemAgregar.count()
            
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
        
        respuesta=r.jasonizar(listaItemAgregar)
        sesion.close()
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"