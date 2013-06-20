from utils import login_required
import flask.views
from flask import jsonify,json
#from flask_weasyprint import HTML, render_pdf
from models.bdCreator import Session
from models.solicitudCambioModelo import SolicitudCambio
from models.itemModelo import Item, Relacion
from models.usuarioModelo import Usuario
from models.faseModelo import Fase
from models.proyectoModelo import Proyecto, comiteProyectoTabla
from models.faseModelo import Fase
from flask.templating import render_template
from flask_weasyprint import HTML, render_pdf

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
    
    
        
class InformeListaItems(flask.views.MethodView):
    """
    Clase que es utilizada para crear el Informe de Costo Economico y Complejidad
    
    """     
    def comaPorPunto(self, string):
        r=''
        for i in string:
            if i==',':
                r=r+'.'
            elif i=='.':
                r=r+','
            else:
                r=r+i
        
        return r
    
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
        if 'idProyecto' not in flask.request.args:
            return "not found"
        idP=flask.request.args.get('idProyecto', '')
        
        #itemsEnSC=sesion.query(Item).join(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idP)).all()
        fasesProyecto=sesion.query(Fase).filter(Fase.idProyecto==int(idP)).all()
        
       
        #auxItem=aux;
        pr=sesion.query(Proyecto).filter(Proyecto.idProyecto==idP).first()
        pl=sesion.query(Usuario).filter(Usuario.id==pr.projectLeaderId).first()
        usuariosComite=sesion.query(Usuario).join(comiteProyectoTabla)\
                                    .filter(Proyecto.idProyecto==idP)\
                                    .filter(Usuario.activo=="true")
        #sesion.close()
        
        
        html=''
        html=html+'<img src="/static/images/blue-23957_640.png" width="250px"\
                            title="Volver a Pagina Principal" \
                            style="cursor: pointer;" />'
        html=html+'<h1 align=center>Informe Items en Proyecto </h1>'
        
        html=html+'<p><b>Proyecto</b>: ' + pr.nombreProyecto + '</p>'
        html=html+'<p><b>Lider de Proyecto</b>: ' + pl.apellidos + ',' + pl.nombres + '[' + pl.username + ']' + ' </p>';
        html=html+'<p><b>Presupuesto</b>: Gs. ' + self.comaPorPunto("{:,}".format( pr.presupuesto))+ '</p>'
        html=html+'<p><b>Miembros del Comite</b>:<br></br> '
        for u in usuariosComite:
            html=html+' - '+ u.apellidos + ', '+u.nombres +' ['+ u.username+ ']<br></br>'
        html=html[0:len(html)-9] 
        html=html+'</p>'
        html=html+'<h2>Fases</h2>'
        html=html+'<p>A continuacion se citan los items clasificados por sus fases correspondientes </p>'
       
        #html=html+'<table border=\'2\' width=\'500\'>'
        #html=html+'<h2>Fases</h2>'
        
        
        for f in fasesProyecto:
            itemsEnFase=sesion.query(Item).filter(Item.idFase==f.idFase).order_by('id asc').all();
            html=html+'<h3>'+f.tag+': ' + f.nombreFase + '</h3>'
            indice=0 
            for i in itemsEnFase:
                indice=indice+1;
                html= html+'<p><b>Item '+str(indice)+'</b></p>'
                html=html+'<table border=\'0\' width=\'500\'>' 
                html= html+'<tr><td>- Nombre item: ' + i.nombreItem + '</td>'
                
                html= html+'<td>- Prioridad: ' + str(i.prioridad) + '</td></tr>'
                html= html+'<tr><td>- Version: ' + str(i.version) + '</td>'
                html= html+'<td>- Costo: Gs. ' + self.comaPorPunto("{:,}".format( i.costo))+ '</td></tr>' 
                
               
                
                html= html+'<tr><td>- Complejidad: ' + str(i.complejidad) + '</td>'
                html= html+'<td>- Estado: ' + i.estado + '</tr></td>'
                html= html+'<tr><td>- Descripcion: ' + i.descripcion + '</td></tr>' 
                html=html + '</table>'
                
            if indice==0:
                html=html + '(Ninguno) <br></br>'
        #html=html+'<h3>Costos detallado</h3> <table id=\'table123\' border=\'2\' width=\'500\'>'
        #html=html+'<tr><th width=\'250\'>Item</th><th>Economico (Gs)</th><th>Complejidad</th></tr>'
    
        html=html+'<p>*<b>Observacion</b>: La escala de prioridad es de 0-19, donde 0 significa la menor prioridad</p>\
          \
         <p>La escala de complejidad es de 0-19, donde 0 significa que no tiene complejidad</p> ' 
        #return render_pdf(HTML(string=html))
        return render_pdf(HTML(string=html))
        #return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"