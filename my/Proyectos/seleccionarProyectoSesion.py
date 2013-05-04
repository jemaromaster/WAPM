from utils import login_required
import flask.views

import flask

        
class SeleccionarProyectoSesion(flask.views.MethodView):

    @login_required
    def get(self): 
        return "nada"
    @login_required
    def post(self):
        
        idProyecto=flask.request.form['idProyecto']
        print "el proyecto es"+ str(idProyecto)
        
        flask.session['idProyecto']=idProyecto
        return "f,Se ha elegido correctamente el proyecto"