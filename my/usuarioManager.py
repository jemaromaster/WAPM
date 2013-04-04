import flask
from utils import login_required

class UsuarioManager(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('usuarioManager.html')
    
    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('usuarioManager'))