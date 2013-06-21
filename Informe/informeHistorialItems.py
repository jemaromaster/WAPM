from utils import login_required
import flask.views
from flask import jsonify,json
#from flask_weasyprint import HTML, render_pdf
from models.bdCreator import Session
from models.solicitudCambioModelo import SolicitudCambio
from models.itemModelo import Item, Relacion
from models.tipoItemModelo import TipoItem
from models.usuarioModelo import Usuario
from models.faseModelo import Fase
from models.proyectoModelo import Proyecto, comiteProyectoTabla
from models.faseModelo import Fase
from flask.templating import render_template
from models.atributosModelo import Atributos
from models.historialModelo import HistorialItem;
from flask.helpers import make_response
from flask_weasyprint import HTML, render_pdf
from models.instanciaAtributos import InstanciaCadena, InstanciaEntero, InstanciaFecha, InstanciaNumerico, InstanciaTipoItem
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
    
    
        
class InformeHistorialItems(flask.views.MethodView):
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
    def format_fecha(self, fecha):
        print("es" + fecha)
        
        r=(fecha[8:10]+"/"+fecha[5:7]+"/"+fecha[0:4])
        return r
    @login_required
    def get(self): 
        
        
        """
        Recibe la peticion de listar el informe, segun los parametros que incluya la peticion.
        @type idSC: string
        @param idSC : parametro que indica el id solicitud de cambio.
        """ 
        #se obtiene los datos de post del server
        
        parametros=['idProyecto', 'idItem'];
        for par in parametros:
            if par not in flask.request.args:
                return make_response('No se enviaron todos los parametros')
        idP=flask.request.args.get('idProyecto', '')
        idI=flask.request.args.get('idItem', '')
        
        #itemsEnSC=sesion.query(Item).join(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idP)).all()
        #fasesProyecto=sesion.query(Fase).filter(Fase.idProyecto==int(idP)).all()
        
       
        #auxItem=aux;
        pr=sesion.query(Proyecto).filter(Proyecto.idProyecto==idP).first()
        pl=sesion.query(Usuario).filter(Usuario.id==pr.projectLeaderId).first()
        '''usuariosComite=sesion.query(Usuario).join(comiteProyectoTabla)\
                                    .filter(Proyecto.idProyecto==idP)\
                                    .filter(Usuario.activo=="true")'''
        #sesion.close()
        
        item=sesion.query(Item).filter(Item.idItem==idI).first()
        faseDelItem=sesion.query(Fase).join(Item).filter(Item.idFase==item.idFase).first()
        itemsEnFase=sesion.query(Item.idItem).filter(Item.idFase==item.idFase).order_by('id asc').all();
        cont=0
        for a in itemsEnFase:
            cont=cont+1
            if(a.idItem==item.idItem):
                break;
        h=sesion.query(HistorialItem).filter(HistorialItem.idItemFK==int(item.idItem)).order_by('id_item_fk asc').all()
        if item.tipoItem_id==None:
            listaAtributo=None
        else:
            listaAtributo=sesion.query(Atributos).filter(Atributos.tipoItemId==int(item.tipoItem_id)).all()
        ti=sesion.query(TipoItem).filter(TipoItem.idTipoItem==item.tipoItem_id).first()
        iti=sesion.query(InstanciaTipoItem)\
                                .filter(InstanciaTipoItem.idItem==int(item.idItem)).all();
        html=''
        html=html+'<img src="/static/images/blue-23957_640.png" width="250px"\
                            style="cursor: pointer;" />'
        html=html+'<h1 align=center>Informe Historial de Item </h1>'
        
        html=html+'<p><b>Proyecto</b>: ' + pr.nombreProyecto + '</p>'
        html=html+'<p><b>Lider de Proyecto</b>: ' + pl.apellidos + ',' + pl.nombres + '[' + pl.username + ']' + ' </p>';
        html=html+'<p><b>Presupuesto</b>: Gs. ' + self.comaPorPunto("{:,}".format( pr.presupuesto))+ '</p>'
        '''html=html+'<p><b>Miembros del Comite</b>:<br></br> '
        for u in usuariosComite:
            html=html+' - '+ u.apellidos + ', '+u.nombres +' ['+ u.username+ ']<br></br>'
        html=html[0:len(html)-9] '''
        #html=html+'</p>'
        html=html+'<p><b>Observacion</b>: '+pr.observacion + '</p>'
        html=html+'<h3>Historial del Item: ' + item.nombreItem + '</h3>'
        html=html+'<p>Codigo : ' + faseDelItem.tag +'.'+ str(cont) + '_' + item.nombreItem+'</p>'
        html=html+'<p>Fase : ' + faseDelItem.nombreFase +'</p>'
        html=html+'<p>Tipo de Item : ' + ti.nombreTipoItem +'</p>'
        html=html+'<b><p>Version ' + str(item.version ) + ' (Actual)</p></b>'
        
        
        html=html+'<table border=\'0\' width=\'500\'>' 
        html= html+'<tr><td>- Nombre item: ' + item.nombreItem + '</td>'
        html= html+'<td>- Prioridad: ' + str(item.prioridad) + '</td></tr>'
        #html= html+'<tr><td>- Version: ' + str(i.version) + '</td>'
        html= html+'<td>- Costo: Gs. ' + self.comaPorPunto("{:,}".format( item.costo))+ '</td></tr>' 
        html= html+'<tr><td>- Complejidad: ' + str(item.complejidad) + '</td>'
        html= html+'<td>- Estado: ' + item.estado + '</tr></td>'
        html= html+'<tr><td>- Descripcion: ' + item.descripcion + '</td></tr>' 
        #html=html+'<p>A continuacion se cita el historial del Itemlos items clasificados por sus fases correspondientes </p>'
       
        #html=html+'<table border=\'2\' width=\'500\'>'
        #html=html+'<h2>Fases</h2>'
        html= html+'<tr><td><b> </b> ' + '</td></tr>' 
        if(listaAtributo is not None and iti is not None):
            for s in iti:
                idt=s.tipoPrimario;
                print('lalalal'+s.tipoPrimario)
                if(idt=='Texto'):
                    aux=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaCadena.version==item.version).first()
                    html=html+'<tr><td>- '+ s.nombreCampo + ': ' + aux.cadena + '</td></tr>'
                    
                elif(idt=='Numerico'):
                    aux=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaNumerico.version==item.version).first()
                    html=html+'<tr><td>- '+ s.nombreCampo + ': ' + str(aux.numerico) + '</td></tr>'
                elif(idt=='Entero'):
                    aux=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                     .filter(InstanciaEntero.version==item.version).first()
                    html=html+'<tr><td>- '+ s.nombreCampo + ': ' + str(aux.entero) + '</td></tr>'
                elif(idt=='Fecha'):
                    aux=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                    .filter(InstanciaFecha.version==item.version).first()
                    fecha_formateada=self.format_fecha(str(aux.fecha))
                    html=html+'<tr><td>- '+ s.nombreCampo + ': ' + fecha_formateada + '</td></tr>'
        
        html= html+'<tr><td><b>Relacionado con (Padres)</b>:' + '</td></tr>' 
        listaRel=sesion.query(Relacion).filter(Relacion.hijo_id==item.idItem).all()
        if(listaRel is not None):
            for f in listaRel:
                i=sesion.query(Item).filter(Item.idItem==f.padre_id).first()
                if(i is None):
                        return make_response ('t,No existe item con ese id')    
                #p=p+json.dumps({"idRelacion": f.idRelacion,"relacion":r_descripcion , "idItemRelacionado":id_item_relacionado,  \
                #                "nombreItem": i.tag , "estado": i.estado}, separators=(',',':'))+",";
                html=html+'<tr><td>__ '+i.tag+' '
            html=html[0:len(html)-1]    
        else:
            html=html+ '<tr><td>'+'(ninguno)'
        html=html+'</td></tr>'
        html=html + '</table>'
        
        #html=html+'<h2>Versiones</h2>'
        
        
        if h is not None:
            for i in h:
                #indice=indice+1;
                html= html+'<p><b>Version '+ str(i.version)+'</b></p>'
                html=html+'<table border=\'0\' width=\'500\'>' 
                html= html+'<tr><td>- Nombre item: ' + i.nombreItem + '</td>'
                html= html+'<td>- Prioridad: ' + str(i.prioridad) + '</td></tr>'
                #html= html+'<tr><td>- Version: ' + str(i.version) + '</td>'
                html= html+'<td>- Costo: Gs. ' + self.comaPorPunto("{:,}".format( i.costo))+ '</td></tr>' 
                html= html+'<tr><td>- Complejidad: ' + str(i.complejidad) + '</td>'
                html= html+'<td>- Estado: ' + i.estado + '</tr></td>'
                html= html+'<tr><td>- Descripcion: ' + i.descripcion + '</td></tr>' 
                #html= html+'<tr><td><b>Datos TipoItem </b>: ' + ti.nombreTipoItem + '</td></tr>' 
                html= html+'<tr><td><b> </b> ' + '</td></tr>' 
                if(listaAtributo is not None and iti is not None):
                    for s in iti:
                        idt=s.tipoPrimario;
                        print('lalalal'+s.tipoPrimario)
                        if(idt=='Texto'):
                            aux=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                             .filter(InstanciaCadena.version==i.version).first()
                            html=html+'<tr><td>- '+ s.nombreCampo + ': ' + aux.cadena + '</td></tr>'
                            
                        elif(idt=='Numerico'):
                            aux=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                             .filter(InstanciaNumerico.version==i.version).first()
                            html=html+'<tr><td>- '+ s.nombreCampo + ': ' + str(aux.numerico) + '</td></tr>'
                        elif(idt=='Entero'):
                            aux=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                             .filter(InstanciaEntero.version==i.version).first()
                            html=html+'<tr><td>- '+ s.nombreCampo + ': ' + str(aux.entero) + '</td></tr>'
                        elif(idt=='Fecha'):
                            aux=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==int(s.idInstanciaTipoItem))\
                                                            .filter(InstanciaFecha.version==i.version).first()
                            fecha_formateada=self.format_fecha(str(aux.fecha))
                            html=html+'<tr><td>- '+ s.nombreCampo + ': ' + fecha_formateada + '</td></tr>'
                    
                from models.historialModelo import HistorialRelacion
                listaRel=sesion.query(HistorialRelacion).filter(HistorialRelacion.versionHijo==int(i.version)).filter(HistorialRelacion.hijo_id==item.idItem)\
                                                        .all()
                html=html+'<tr><td>- <b>Relacionado con (Padres)</b>: </td></tr> '
                entro=False
                for f in listaRel:
                    entro=True
                    i=sesion.query(Item).filter(Item.idItem==f.padre_id).first()
                    if(i is None):
                            return make_response ('t,No existe item con ese id')    
                    #p=p+json.dumps({"idRelacion": f.idRelacion,"relacion":r_descripcion , "idItemRelacionado":id_item_relacionado,  \
                    #                "nombreItem": i.tag , "estado": i.estado}, separators=(',',':'))+",";
                    html=html+'<tr><td>__ '+i.tag+' '
               
                if entro is False:
                    html=html+ '<tr><td>'+'(Ninguno)'
                html=html+'</td></tr>'
                html=html + '</table>'
        else:
            html=html + '(El item no cuenta con version) <br></br>'
                
        
        #html=html+'<h3>Costos detallado</h3> <table id=\'table123\' border=\'2\' width=\'500\'>'
        #html=html+'<tr><th width=\'250\'>Item</th><th>Economico (Gs)</th><th>Complejidad</th></tr>'
    
        html=html+'<p>*<b>Observacion</b>: La escala de prioridad es de 0-19, donde 0 significa la menor prioridad</p>\
          \
         <p>La escala de complejidad es de 0-19, donde 0 significa que no tiene complejidad</p> ' 
        #return render_pdf(HTML(string=html))
        sesion.close()
        return render_pdf(HTML(string=html))
        #return respuesta
        
      
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"