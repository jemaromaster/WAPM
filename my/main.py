import flask, flask.views
from flask import jsonify

from remote import Remote
from usuarioManager import UsuarioManager
from agregarUsuario import AgregarUsuario
from modificarUsuario import ModificarUsuario
from inactivarUsuario import InactivarUsuario

from proyectoManager import ProyectoManager
from modificarProyecto import ModificarProyecto
from agregarProyecto import AgregarProyecto
from listarProyecto import ListarProyectos

from login import Login
from listarUsuarios import ListarUsuarios
from crearUsuario import CrearUsuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bdCreator import initDB

from agregarMiembrosProyecto import AgregarMiembrosProyecto
app = flask.Flask(__name__)
"""
Se realizan las redirecciones de las peticiones de manera conveniente. Cada peticion
entrante debe estar asociada a una URL, con dicha URL la peticion es canalizada a travez
de las reglas de URL a las funciones que se haran cargo de senrvirlas
"""
initDB()
# Don't do this
app.secret_key = "bacon"

app.add_url_rule('/',
                 view_func=Login.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/usuarioManager/',
                 view_func=UsuarioManager.as_view('usuarioManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/proyectoManager/',
                 view_func=ProyectoManager.as_view('proyectoManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarUsuarios/',
                 view_func=ListarUsuarios.as_view('listarUsuarios'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarUsuario/',
                 view_func=AgregarUsuario.as_view('agregarUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/usuarioManager/modificarUsuario',
                 view_func=ModificarUsuario.as_view('modificarUsuario'),
                 methods=["GET", "POST"])


app.add_url_rule('/agregarProyecto/',
                 view_func=AgregarProyecto.as_view('agregarProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/modificarProyecto',
                 view_func=ModificarProyecto.as_view('modificarProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarProyectos/',
                 view_func=ListarProyectos.as_view('listarProyectos'),
                 methods=["GET", "POST"])

#ESTO corresponde a many to many de agregar proyecto
'''app.add_url_rule('/agregarMiembrosProyecto/',
                 view_func=AgregarMiembrosProyecto.as_view('agregarMiembrosProyecto'),
                 methods=["GET", "POST"])'''



app.debug = True
app.run()