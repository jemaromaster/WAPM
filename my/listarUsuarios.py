from utils import login_required
import flask
from flask import jsonify


class ListarUsuarios(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('remote.html')
        
    @login_required
    def post(self):
        return jsonify(username="jesus",
                   email="lalaal",
                   id="42")
