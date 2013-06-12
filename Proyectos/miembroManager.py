import flask
import flask.views
from utils import login_required
from utils import rolPL_required
class MiembroManager(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html usuarioManager, relacionada a 
    cuestiones de mantenimiento de usuarios del sistema
    """
    @login_required
    @rolPL_required
    def get(self):
        return flask.render_template('MiembroProyectoManager.html')