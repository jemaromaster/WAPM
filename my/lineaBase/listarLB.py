from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.lineaBaseModelo import LineaBase 
sesion=Session()


class Respuesta():
    """
    Clase utilizada cuando se hace una peticion de listado de 
    roles de proyecto al servidor. Se obtienen de la bd las filas a 
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
    
    def jasonizar(self, listaLB):
        """
        modulo que jasoniza la respuesta
        """
        p='' 
        pre="{\"totalpages\": \""+str(self.totalPages) + "\",\"currpage\" : \"" + str(self.currPage) + "\",\"totalrecords\" : \"" 
        pre= pre + str(self.totalRecords) + " \",\"invdata\" : [" 
        
        
        for lb in listaLB:
            p=p+"{\"idLB\":\""+str(lb.id)+"\",\"descripcion\": \""+lb.descripcion +"\",\"estado\": \""+lb.estado+"\"},"
            # {"nombre":"nombre","idRol":"rol","descripcion":"descripciones"},
        p=p[0:len(p)-1]    
        p=p+"]}"    
        p=pre+p
        
        return p 
        
class ListarLB(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        search=flask.request.args.get('_search', '')
        param1=flask.request.args.get('page', '')
        param2=flask.request.args.get('rows', '')
        idFase=flask.request.args.get('idFase', '') 
        if(idFase == '' or idFase == '0'):
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