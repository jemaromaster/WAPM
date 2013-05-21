import flask
import flask.views
from utils import login_required

class EstadoFase(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html usuarioManager, relacionada a 
    cuestiones de mantenimiento de usuarios del sistema
    """
    @login_required
    def get(self):
        return flask.render_template('estadoFase.html')
    
    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('fasesManager'))