import flask
import flask.views
from utils import login_required
from utils import rolAdmin_required

class RolUsuario(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html rolProyectoManager, relacionada a 
    cuestiones de mantenimiento de los roles de proyecto
    """
    @login_required
    @rolAdmin_required
    def get(self):
        return flask.render_template('rolUsuarioManager.html')