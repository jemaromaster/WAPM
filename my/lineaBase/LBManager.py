import flask
import flask.views
from utils import login_required

class LBManager(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html lineaBaseManager, relacionada a 
    cuestiones de mantenimiento de los roles de proyecto
    """
    @login_required
    def get(self):
        return flask.render_template('lineaBaseManager.html')