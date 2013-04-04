from utils import login_required
import flask


class Remote(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('remote.html')
        
    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('remote'))