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
    
    def jasonizar(self, listaFase):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        
        for fase in listaFase:
            p=p+"{\"idFase\": \""+str(fase.idFase)+"\",\"nombreFase\": \""+ \
                fase.nombreFase+ \
                "\",\"fechaInicio\": \""+str(fase.fechaInicio)+"\", \"fechaFinalizacion\": \""+ \
                str(fase.fechaFinalizacion) +\
                "\", \"descripcion\": \""+fase.descripcion+"\", \"estado\":\"" + fase.estado +\
                "\",\"idProyecto\":\"" + str(fase.idProyecto) + "\"},"
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        return p 
        
class ListarComboFases(flask.views.MethodView):        
    @login_required
    def post(self):
        idProyecto=flask.request.form['idProyecto']
        print "id proyecto en listar combo fases:  " + idProyecto
        if(idProyecto=='' or idProyecto=='0'):
            return "[]"
        
        lf=sesion.query(Fase).filter(Fase.idProyecto==int(idProyecto))
        prejsonF='['
        jsonF=''
        for fase in lf:
            jsonF=jsonF+"{\"idFase\":\""+str(fase.idFase)+"\",\"nombreFase\":\""+fase.nombreFase+"\"},"
        jsonF=jsonF[0:len(jsonF)-1]    
        jsonF=prejsonF+jsonF+"]"        
        return jsonF
        
        

class ListarFases(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idProyecto=flask.request.args.get('idProyecto', '')
        
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
                                                    .filter(Fase.idProyecto==flask.session['idProyecto'])\
                                                    .filter(Fase.nombreFase.like(nombreFase))\
                                                    .filter(Fase.estado.like(estado))[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
            total=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==flask.session['idProyecto'])\
                                                    .filter(Fase.nombreFase.like(nombreFase))\
                                                    .filter(Fase.estado.like(estado)).count()
                
        else:
            #si no hubo filtro entonces se envian los datos de usuarios activos
            
             print 'el id proyeceeecto es' + str(idProyecto)
             listaFase=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==flask.session['idProyecto'])[desde:hasta]
                                                    #.filter(Proyecto.projectLeaderId==projectLeaderId)
             total=sesion.query(Fase).order_by(filtrarPor)\
                                                    .filter(Fase.idProyecto==flask.session['idProyecto']).count()
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
        return respuesta
        
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"