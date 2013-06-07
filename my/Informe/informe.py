from utils import login_required
import flask.views
from flask import jsonify,json
from models.bdCreator import Session
from models.solicitudCambioModelo import SolicitudCambio
from models.itemModelo import Item, Relacion
from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto
from models.faseModelo import Fase
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
    
    
        
class Informe(flask.views.MethodView):
    """
    Clase que es utilizada para crear el Informe de Costo Economico y Complejidad
    
    """     
    def jasonizar(self, lista):
        """
        Modulo que jasoniza la respuesta.
        @type  lista: json
        @param lista: Incluye los resultados que seran enviados al lado cliente para mostrar el informe 
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
    def recorrerHijos(self, i, dicTotal, dicDelItem):
        #se obtienen todos los hijos
        dicTotal[i.idItem]=i;
        dicDelItem[i.idItem]=i;
        s=sesion.query(Item).filter(Relacion.padre_id==i.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all()
        
        if (s!=None): #si es que es el ultimo elemento de la LB
            for son in s:
                self.recorrerHijos(son, dicTotal, dicDelItem)
        
        return 
        
    def armarHtml(self, nombreItem, sc, scpj):
        r='<tr>'
        r=r+'<td>'+nombreItem + ': </td>'+'<td>CE:'+str(sc)+ '</td>'+'<td>CC:'+str(scpj) +     '</td>'
        r=r+'</tr>'
        
        return r;
    @login_required
    def get(self): 
        
        
        """
        Recibe la peticion de listar el informe, segun los parametros que incluya la peticion.
        @type idSC: string
        @param idSC : parametro que indica el id solicitud de cambio.
        """ 
        #se obtiene los datos de post del server
        idSC=flask.request.args.get('idSC', '')
        
        itemsEnSC=sesion.query(Item).join(SolicitudCambio.items).filter(SolicitudCambio.id==int(idSC)).all()
        sc=sesion.query(SolicitudCambio).filter(SolicitudCambio.id==int(idSC)).first()
        
        autor=sesion.query(Usuario).filter(Usuario.id==sc.idSolicitante).first()
        
        
        
        dTotal=dict()
        dLista=dict()
        aux=None;
        for i in itemsEnSC:
            dItem=dict()
            self.recorrerHijos(i, dTotal, dItem)     
            dLista[i.idItem]=dItem;
            aux=i
            
        auxItem=aux;
        pr=sesion.query(Proyecto).join(Fase).join(Item).filter(Item.idItem==auxItem.idItem).first()
        sesion.close()
        
        html=''
        html=html+'<h1>Informe de Costo</h1><p><b>Motivo de Solicitud de Cambio</b>:'+sc.descripcion+'</p><p><b>Solicitante</b>:Username:'+autor.username+'</p>' + '<p>   Nombre:'+autor.nombres +    '   Apellido: '+ autor.apellidos   +   '</p>'
        
        html=html+'<p><b>Proyecto</b>: ' + pr.nombreProyecto + '</p>'
        html=html+'<p><b>Presupuesto</b>: ' + str(pr.presupuesto) + '</p>'
        html=html+'<h3>Items involucrados</h3>'
        html=html+'<p>A continuacion se citan los items involucrados en el calculo de costos (economico y complejidad)<br></br> junto con sus descendientes </p>'
        html=html+'<table border=\'2\' width=\'500\'>'
        html=html+'<tr><th width=\'200\'>Item En Solicitud</th><th>Descendientes</th></tr>'
        for index in dLista.keys():
            html=html+'<tr><td>'+dLista[index][index].nombreItem
            html=html+'</td>'
            html=html+'<td>'
            bandera=0;
            for i2 in dLista[index].keys():
                item=dLista[index][i2]
                bandera=1;
                if(item.idItem!=index):
                    html=html+item.nombreItem+', '
            
            html=html[0:len(html)-2] 
            if bandera==0:
                html=html+'Ninguno'
            html=html+'</td></tr>'
            
        html=html+'</table>'
        html=html+'<br></br><h3>Costos detallado</h3> <table border=\'2\' width=\'500\'>'
        html=html+'<tr><th width=\'250\'>Item</th><th>Economico (Gs)</th><th>Complejidad</th></tr>'
        for index in dLista.keys():
            sumacosto=0
            sumacpj=0
            for i2 in dLista[index].keys():
                item=dLista[index][i2]
                sumacosto=sumacosto+item.costo
                sumacpj=sumacpj+item.complejidad
                
            html=html+self.armarHtml(dLista[index][index].nombreItem, sumacosto, sumacpj)
        
        ce=0;
        cpj=0;
        for ind in dTotal.keys():
            ce=ce+dTotal[ind].costo;
            cpj=cpj+dTotal[ind].complejidad;
        
        html=html+self.armarHtml("<b>Total</b>", ce, cpj)
        html=html+'</table>'
        html=html+'<p>*Observacion: El calculo de costo (economico y complejidad) se obtiene a partir de la suma</p><p>\
         de todos los descendientes del item respectivos incluyendo el item</p> \
         <p>La escala de complejidad es de 0-99, donde 0 significa que no tiene complejidad</p> ' 
        respuesta='{"html":"'+ html + '"}'
        return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"