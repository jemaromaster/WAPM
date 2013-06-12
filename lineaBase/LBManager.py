import flask
import flask.views
from utils import login_required

class LBManager(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html lineaBaseManager, relacionada a 
    cuestiones de mantenimiento de las lineas bases en un proyecto
    """
    @login_required
    def get(self):
        """
        Metodo que devuelve la pagina html solicitada. En este caso devuelve la pagina lineaBaseManager.html
        """
        return flask.render_template('lineaBaseManager.html')