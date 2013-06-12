import flask
import flask.views
from utils import login_required

class EstadoFase(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html estadoFase.hml, 
    donde se listan las fases dentro del proyecto seleccionado con sus respectivos estados
    """
    @login_required
    def get(self):
        """
        Metodo utilizado para devolver al cliente la pagina estadoFase.hml
        """
        return flask.render_template('estadoFase.html')
    
    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('fasesManager'))