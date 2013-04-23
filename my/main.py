import flask, flask.views
from flask import jsonify


from Usuarios.usuarioManager import UsuarioManager
from Usuarios.agregarUsuario import AgregarUsuario
from Usuarios.modificarUsuario import ModificarUsuario
from Usuarios.listarUsuarios import ListarUsuarios

from Proyectos.proyectoManager import ProyectoManager
from Proyectos.modificarProyecto import ModificarProyecto
from Proyectos.agregarProyecto import AgregarProyecto
from Proyectos.listarProyecto import ListarProyectos
from Proyectos.agregarMiembrosProyecto import AgregarMiembrosProyecto
from Proyectos.listarMiembrosProyecto import ListarMiembrosProyecto


from login import Login

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bdCreator import initDB
from models import poblarBD
 
app = flask.Flask(__name__)
"""
Se realizan las redirecciones de las peticiones de manera conveniente. Cada peticion
entrante debe estar asociada a una URL, con dicha URL la peticion es canalizada a travez
de las reglas de URL a las funciones que se haran cargo de senrvirlas
"""
initDB()
poblarBD.cargaEstatica()

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

app.add_url_rule('/listarMiembrosProyecto/',
                 view_func=ListarMiembrosProyecto.as_view('listarMiembrosProyecto'),
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

#Corresponde a agregar Miembro de proyecto
app.add_url_rule('/agregarMiembrosProyecto/',
                 view_func=AgregarMiembrosProyecto.as_view('agregarMiembrosProyecto'),
                 methods=["GET", "POST"])


app.debug = True
app.run()