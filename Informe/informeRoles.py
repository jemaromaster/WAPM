from utils import login_required, rolPL_required
import flask.views
from flask import jsonify,json
from flask_weasyprint import HTML, render_pdf
from models.bdCreator import Session
from models.solicitudCambioModelo import SolicitudCambio
from models.solicitudCambioModelo import Voto
from models.itemModelo import Item, Relacion
from models.rolProyectoModelo import RolProyecto
from models.usuarioModelo import Usuario
from models.proyectoModelo import Proyecto, comiteProyectoTabla
from models.faseModelo import Fase
from models.lineaBaseModelo import LineaBase

sesion=Session()


class InformeRoles(flask.views.MethodView):
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
        html=html+"<h3>Informe de Roles</h3></tr>"
        proyecto=sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).first()
        lider=sesion.query(Usuario).join(Proyecto).filter(Usuario.id==Proyecto.projectLeaderId).first()
        
        html=html+"<tr><td><h4>Proyecto:    "+proyecto.nombreProyecto+"</h4></td></tr></table>"
        
        idUsuario=flask.session['idUsuario']
        esComite=0
        esComite=esComite+sesion.query(Usuario).join(Proyecto).count()
        
        
        
        if esComite==0:
            html=html+"<table><tr><td><h4>No forma Parte del Comite de Cambios</h4></td></tr>"
        else:
            html=html+"<table><tr><td><h4>Parte del Comite de Cambios</h4></td></tr>"
        if lider.id==idUsuario:
            html=html+"<tr><td><h4>Es Project Leader: Posee todos los permisos</h4></td></tr></table>"
        else:
            html=html+"</table><br></br>"
            
            fases=sesion.query(Fase).order_by("fase.id asc").filter(Fase.idProyecto==idProyecto).all()
            for fase in fases:
                html=html+"<div><hr></hr></div>"
                html=html+"<br></br><h3>Fase: "+fase.tag+"  "+fase.nombreFase+"</h3><div><table>"
                roles=sesion.query(RolProyecto).join(RolProyecto.usuarios).filter(Usuario.id==idUsuario,RolProyecto.idFase==fase.idFase).all()
                for rol in roles:
                    html=html+"<tr><td><h5>Rol: "+rol.nombre+"</h5></td><td><h5>____Descripcion: "+rol.descripcion+"</h5></td></tr>"
                html=html+"</table></div>"
        return render_pdf(HTML(string=html))