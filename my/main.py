import flask, flask.views
from flask import jsonify


from Usuarios.usuarioManager import UsuarioManager
from Usuarios.agregarUsuario import AgregarUsuario
from Usuarios.modificarUsuario import ModificarUsuario
from Usuarios.listarUsuarios import ListarUsuarios

from Proyectos.proyectoManager import ProyectoManager
from Proyectos.modificarProyecto import ModificarProyecto
from Proyectos.agregarProyecto import AgregarProyecto
from Proyectos.listarProyecto import ListarProyectos, ListarProyectosCombo
from Proyectos.agregarMiembrosProyecto import AgregarMiembrosProyecto
from Proyectos.listarMiembrosProyecto import ListarMiembrosProyecto
from Proyectos.quitarMiembrosProyecto import QuitarMiembrosProyecto
from Proyectos.miembroManager import MiembroManager

from Fases.faseManager import FaseManager
from Fases.agregarFase import AgregarFase
from Fases.modificarFase import ModificarFase 
from Fases.listarFases import ListarFases
from Fases.listarFases import ListarComboFases

from rol_proyecto.rolProyectoManager import RolProyectoManager
from rol_proyecto.listarRolProyecto import ListarRolProyecto
from rol_proyecto.agregarRolProyecto import AgregarRolProyecto
from rol_proyecto.modificarRolProyecto import ModificarRolProyecto
from rol_proyecto.listarPermiso_Rol import ListarPermisosRol
from rol_proyecto.agregarPermisoRol import AgregarPermisoRol
from rol_proyecto.quitarPermisoRol import QuitarPermisoRol

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


app.add_url_rule('/agregarProyecto/',
                 view_func=AgregarProyecto.as_view('agregarProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/modificarProyecto',
                 view_func=ModificarProyecto.as_view('modificarProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarProyectos/',
                 view_func=ListarProyectos.as_view('listarProyectos'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarProyectoCombo/',
                 view_func=ListarProyectosCombo.as_view('listarProyectoCombo'),
                 methods=["GET", "POST"])

#Corresponde a agregar Miembro de proyecto
app.add_url_rule('/agregarMiembrosProyecto/',
                 view_func=AgregarMiembrosProyecto.as_view('agregarMiembrosProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarMiembrosProyecto/',
                 view_func=ListarMiembrosProyecto.as_view('listarMiembrosProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/QuitarMiembrosProyecto',
                 view_func=QuitarMiembrosProyecto.as_view('quitarMiembrosProyecto'),
                 methods=["GET", "POST"])

#fases
app.add_url_rule('/agregarFase/',
                 view_func=AgregarFase.as_view('agregarFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/faseManager/',
                 view_func=FaseManager.as_view('faseManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarFases/',
                 view_func=ListarFases.as_view('listaFases'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarComboFases/',
                 view_func=ListarComboFases.as_view('listarComboFases'),
                 methods=["GET", "POST"])
app.add_url_rule('/modificarFase/',
                 view_func=ModificarFase.as_view('modificarFase'),
                 methods=["GET", "POST"])

#roles de proyecto
app.add_url_rule('/rolProyectoManager/',
                 view_func=RolProyectoManager.as_view('rolProyectoManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarRolProyecto/',
                 view_func= ListarRolProyecto.as_view('listarRolProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarPermisosRol/',
                 view_func= ListarPermisosRol.as_view('listarPermisosRol'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarRolProyecto/',
                 view_func=AgregarRolProyecto.as_view('agregarRolProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/modificarRolProyecto/',
                 view_func=ModificarRolProyecto.as_view('modificarRolProyecto'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarPermisoRol/',
                 view_func=AgregarPermisoRol.as_view('agregarPermisoRol'),
                 methods=["GET", "POST"])
app.add_url_rule('/quitarPermisoRol/',
                 view_func=QuitarPermisoRol.as_view('quitarPermisoRol'),
                 methods=["GET", "POST"])

app.add_url_rule('/miembroManager/',
                 view_func=MiembroManager.as_view('miembroManager'),
                 methods=["GET", "POST"])

app.debug = True
app.run()