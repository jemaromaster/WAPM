from utils import login_required
import flask.views
import flask
from models.bdCreator import Session
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario

        
class SeleccionarProyectoSesion(flask.views.MethodView):

    @login_required
    def get(self): 
        return "nada"
    @login_required
    def post(self):
        
        idProyecto=flask.request.form['idProyecto']
        print "el proyecto es"+ str(idProyecto)
        
        flask.session['idProyecto']=idProyecto
        
        sesion=Session()
        idProyectoSeleccion=flask.session['idProyecto']
        idUsuario=flask.session['idUsuario']
        comiteProject=sesion.query(Usuario.id).filter(Proyecto.idProyecto==idProyectoSeleccion).join(Proyecto.usuariosComite)\
                                          .filter(Usuario.id==idUsuario).first();
        sesion.close()
        if comiteProject is None:
            flask.session['esComite']=0
        else:
            flask.session['esComite']=1
        print "valor de comite es:   " + str(flask.session['esComite'])     
        return str(flask.session['esComite'])