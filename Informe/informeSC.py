from utils import login_required, rolPL_required
import flask.views
from flask import jsonify,json
from flask_weasyprint import HTML, render_pdf
from models.bdCreator import Session
from models.solicitudCambioModelo import SolicitudCambio
from models.solicitudCambioModelo import Voto
from models.itemModelo import Item, Relacion
from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto, comiteProyectoTabla
from models.faseModelo import Fase
from models.lineaBaseModelo import LineaBase

sesion=Session()


class InformeSC(flask.views.MethodView):
    @login_required
    @rolPL_required
    def get(self): 
         #se obtiene los datos de post del server
        idProyecto=flask.request.args.get('idProyecto', '')
        
        if idProyecto=='' or idProyecto == None:
            return
        idProyecto=int(idProyecto)
        #html=self.getHead()
        html=''
        html="<table><tr><td><div><img src='/static/images/blue-23957_640.png' width='150px'/></div></td><td>"
        html=html+"<h3>Informe de Solicitudes de Cambio</h3></tr>"
        proyecto=sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).first()
        lider=sesion.query(Usuario).join(Proyecto).filter(Usuario.id==Proyecto.projectLeaderId).first()
        html=html+"<tr><td><h4>Proyecto:    "+proyecto.nombreProyecto+"</h4></td><td><h4> Lider:    "+lider.username+  "</h4></td></tr></table>"
        solicitudes=sesion.query(SolicitudCambio).filter(SolicitudCambio.idProyecto==idProyecto).all()
        for solicitud in solicitudes:
            
            
            
            html=html+"<div><hr></hr></div>"
            html=html+"<div><table>"
            html=html+"<tr><td><h5>Solicitud: "+solicitud.descripcion+"</h5></td><td><h5>Estado: "+solicitud.estado+"</h5></td></tr>"
            solicitante=sesion.query(Usuario).filter(Usuario.id==solicitud.idSolicitante).first()
            html=html+"<tr><td><h5>Solicitante: "+solicitante.apellidos+", "+solicitante.nombres+" ["+solicitante.username+"]</h5></td></tr>"
            votos=sesion.query(Voto).filter(Voto.solicitud==solicitud.id).all()
            html=html+"<tr><td><h5>Votantes:</h5></td></tr>"
            html=html+"</table></div>"
            html=html+"<div><table>"
            for voto in votos:
                votante=sesion.query(Usuario).filter(Usuario.id==voto.votante).first()
                html=html+"<tr><td><p>Votante: "+votante.apellidos+", "+votante.nombres+" ["+votante.username+"]</p></td>"
                elVoto=''
                if voto.voto=="si":
                    elVoto="Aprobar"
                elif voto.voto=="no":
                    elVoto="Rechazar"
                elif voto.voto=="p":
                    elVoto="Pendiente"
                html=html+"<td>_____</td><td><p>Voto:   "+elVoto+"</p><td></tr> "
            html=html+"</table></div>"
            lbRotas=sesion.query(LineaBase).filter(LineaBase.scAfecto==solicitud.id).all()
            html=html+"<div><table>"
            html=html+"<tr><td><h5>Linea/s Base/s Afectada/s</h5></td></tr>"
            for lb in lbRotas:
                fase=sesion.query(Fase).filter(Fase.idFase==lb.idFase).first()
                html=html+"<tr><td><p>Fase: "+fase.tag+"____Linea Base: "+lb.descripcion+"</p></td>"
            html=html+"</table></div>"
        return render_pdf(HTML(string=html))