import flask, flask.views
from flask import jsonify

from remote import Remote
from usuarioManager import UsuarioManager
from login import Login
from listarUsuarios import ListarUsuarios
from crearUsuario import CrearUsuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from models.db_def import Album, Artist, engine


app = flask.Flask(__name__)
# Don't do this
app.secret_key = "bacon"

app.add_url_rule('/',
                 view_func=Login.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/crearUsuario/',
                 view_func=CrearUsuario.as_view('crearUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/remote/',
                 view_func=Remote.as_view('remote'),
                 methods=['GET', 'POST'])
app.add_url_rule('/usuarioManager/',
                 view_func=UsuarioManager.as_view('usuarioManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarUsuarios/',
                 view_func=ListarUsuarios.as_view('listarUsuarios'),
                 methods=["GET", "POST"])

app.debug = True
app.run()