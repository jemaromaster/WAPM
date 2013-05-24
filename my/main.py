import flask, flask.views
from flask import jsonify

from lineaBase.LBManager import LBManager
from lineaBase.agregarLB import AgregarLB
from lineaBase.modificarLB import ModificarLB
from lineaBase.listarLB import ListarLB
from lineaBase.listarItemsLB import ListarItemBase
from lineaBase.agregarItem import AgregarItemLB
from lineaBase.cerrarLB import CerrarLB

from Usuarios.usuarioManager import UsuarioManager
from Usuarios.agregarUsuario import AgregarUsuario
from Usuarios.modificarUsuario import ModificarUsuario
from Usuarios.listarUsuarios import ListarUsuarios
from Usuarios.listarUsuarios import ListarComboUsuarios

from Proyectos.finalizarProyecto import FinalizarProyecto
from Proyectos.proyectoManager import ProyectoManager
from Proyectos.modificarProyecto import ModificarProyecto
from Proyectos.agregarProyecto import AgregarProyecto
from Proyectos.listarProyecto import ListarProyectos, ListarProyectosCombo
from Proyectos.listarProyecto import ListarProyectos, ListarProyectosComboBase
from Proyectos.agregarMiembrosProyecto import AgregarMiembrosProyecto
from Proyectos.listarMiembrosProyecto import ListarMiembrosProyecto
from Proyectos.quitarMiembrosProyecto import QuitarMiembrosProyecto
from Proyectos.agregarMiembrosComite import AgregarMiembrosComite
from Proyectos.listarMiembrosComite import ListarMiembrosComite
from Proyectos.quitarMiembrosComite import QuitarMiembrosComite
from Proyectos.miembroManager import MiembroManager
from Proyectos.activarProyecto import ActivarProyecto

from Proyectos.listarProyectosComboBox import ListarProyectosComboBox
from Proyectos.seleccionarProyectoSesion import SeleccionarProyectoSesion

from Fases.finalizarFase import FinalizarFase
from Fases.estadoFase import EstadoFase
from Fases.listarItems import ListarItemsFase
from Fases.agregarFase import AgregarFase
from Fases.modificarFase import ModificarFase 
from Fases.listarFases import ListarFases
from Fases.listarFases import ListarComboFases
from Fases.listarFasesComboBox import ListarFasesComboBox

from TiposDeItem.tipoItemManager import TipoItemManager
from TiposDeItem.agregarTipoItem import AgregarTipoItem
from TiposDeItem.listarTipoItem import ListarTipoItem
from TiposDeItem.modificarTipoItem import ModificarTipoItem

from rol_proyecto.rolProyectoManager import RolProyectoManager
from rol_proyecto.listarRolProyecto import ListarRolProyecto
from rol_proyecto.agregarRolProyecto import AgregarRolProyecto
from rol_proyecto.modificarRolProyecto import ModificarRolProyecto
from rol_proyecto.listarPermiso_Rol import ListarPermisosRol
from rol_proyecto.agregarPermisoRol import AgregarPermisoRol
from rol_proyecto.quitarPermisoRol import QuitarPermisoRol
from rol_proyecto.rolUsuarioManager import RolUsuario
from rol_proyecto.listarRolUsuario import ListarRolUsuario
from rol_proyecto.agregarRolUsuario import AgregarRolUsuario
from rol_proyecto.quitarRolUsuario import QuitarRolUsuario
from rol_proyecto.estadoRol import EstadoRol


from Items.listarTipoItemComboBox import ListarTipoItemComboBox
from Items.itemManager import ItemManager
from Items.agregarItem import AgregarItem
from Items.listarItems import ListarItems
from Items.listarAtributosResultado import ListarAtributosResultado
from Items.modificarItem import ModificarItem
from Items.listarDatosItemVersion import ListarDatosItemVersion
from Items.eliminarRevivirAprobarItem import EliminarRevivirAprobarItem
from Items.listarItemsRelacionarMiniDialogoComboBox import ListarItemsRelacionarMiniDialogoComboBox
from Items.agregarRelacion import AgregarRelacion
from Items.listarRelaciones import ListarRelaciones
from Items.eliminarRelacion import EliminarRelacion
from Items.adjuntarArchivo import AdjuntarArchivo
from login import Login
from miembros import Miembros

from TiposDeItem.listarAtributo import ListarAtributo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bdCreator import initDB
from models import poblarBD
 
app = flask.Flask(__name__)
"""
template_folder='/home/jesus/git/WAPM_rolProyectoiter3/my/templates/'
Se realizan las redirecciones de las peticiones de manera conveniente. Cada peticion
entrante debe estar asociada a una URL, con dicha URL la peticion es canalizada a travez
de las reglas de URL a las funciones que se haran cargo de senrvirlas
"""

initDB() 
poblarBD.cargaEstatica() 
#
#poblarBD.cargarUsuarios(10) 
#poblarBD.cargarProyecto()
# Don't do this
app.secret_key = "bacon"
app.add_url_rule('/',
                 view_func=Login.as_view('index'),
                 methods=["GET", "POST"])

app.add_url_rule('/miembros/',
                 view_func=Miembros.as_view('miembros'),
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

app.add_url_rule('/listarComboUsuario/',
                 view_func=ListarComboUsuarios.as_view('listarComboUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarUsuario/',
                 view_func=AgregarUsuario.as_view('agregarUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/usuarioManager/modificarUsuario',
                 view_func=ModificarUsuario.as_view('modificarUsuario'),
                 methods=["GET", "POST"])


app.add_url_rule('/finalizarProyecto/',
                 view_func=FinalizarProyecto.as_view('finalizarProyecto'),
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
app.add_url_rule('/listarProyectoComboBase/',
                 view_func=ListarProyectosComboBase.as_view('listarProyectoComboBase'),
                 methods=["GET", "POST"])
app.add_url_rule('/activarProyecto/',
                 view_func=ActivarProyecto.as_view('activarProyecto'),
                 methods=["POST"])

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

#Corresponde a agregar Miembro Comite
app.add_url_rule('/agregarMiembrosComite/',
                 view_func=AgregarMiembrosComite.as_view('agregarMiembrosComite'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarMiembrosComite/',
                 view_func=ListarMiembrosComite.as_view('listarMiembrosComite'),
                 methods=["GET", "POST"])
app.add_url_rule('/quitarMiembrosComite',
                 view_func=QuitarMiembrosComite.as_view('quitarMiembrosComite'),
                 methods=["GET", "POST"])

#fases
app.add_url_rule('/finalizarFase/',
                 view_func=FinalizarFase.as_view('finalizarFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/estadoFase/',
                 view_func=EstadoFase.as_view('estadoFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarFase/',
                 view_func=AgregarFase.as_view('agregarFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarFases/',
                 view_func=ListarFases.as_view('listaFases'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarItemsFase/',
                 view_func=ListarItemsFase.as_view('listaItemsFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarComboFases/',
                 view_func=ListarComboFases.as_view('listarComboFases'),
                 methods=["GET", "POST"])
app.add_url_rule('/modificarFase/',
                 view_func=ModificarFase.as_view('modificarFase'),
                 methods=["GET", "POST"])
app.add_url_rule('/tipoItemManager/',
                 view_func=TipoItemManager.as_view('tipoItemManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarTipoItem/',
                 view_func=AgregarTipoItem.as_view('agregarTipoItem'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarTipoItem/',
                 view_func=ListarTipoItem.as_view('listarTipoItem'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarAtributo/',
                 view_func=ListarAtributo.as_view('listarAtributo'),
                 methods=["GET", "POST"])

app.add_url_rule('/modificarTipoItem/',
                 view_func=ModificarTipoItem.as_view('modificarTipoItem'),
                 methods=["GET", "POST"])

app.add_url_rule('/listarProyectosComboBox/',
                 view_func=ListarProyectosComboBox.as_view('listarProyectosComboBox'),
                 methods=["GET", "POST"])

app.add_url_rule('/seleccionarProyectoSesion/',
                 view_func=SeleccionarProyectoSesion.as_view('seleccionarProyectoSesion'),
                 methods=["GET", "POST"])

app.add_url_rule('/listarFasesComboBox/',
                 view_func=ListarFasesComboBox.as_view('listarFasesComboBox'),
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
app.add_url_rule('/rolUsuarioManager/',
                 view_func=RolUsuario.as_view('rolUsuarioManager'),
                 methods=["GET", "POST"])
app.add_url_rule('/listarRolUsuario/',
                 view_func=ListarRolUsuario.as_view('listarRolUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/agregarRolUsuario/',
                 view_func=AgregarRolUsuario.as_view('agregarRolUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/quitarRolUsuario/',
                 view_func=QuitarRolUsuario.as_view('quitarRolUsuario'),
                 methods=["GET", "POST"])
app.add_url_rule('/estadoRol/',
                 view_func=EstadoRol.as_view('estadoRol'),
                 methods=["GET", "POST"])


app.add_url_rule('/miembroManager/',
                 view_func=MiembroManager.as_view('miembroManager'),
                 methods=["GET", "POST"])

app.add_url_rule('/listarTipoItemComboBox/',
                 view_func=ListarTipoItemComboBox.as_view('listarTipoItemComboBox'),
                 methods=["GET"])

app.add_url_rule('/itemManager/',
                 view_func=ItemManager.as_view('itemManager'),
                 methods=["GET"])

app.add_url_rule('/agregarItem/',
                 view_func=AgregarItem.as_view('agregarItem'),
                 methods=["POST"])

app.add_url_rule('/listarItems/',
                 view_func=ListarItems.as_view('listarItems'),
                 methods=["GET"])

app.add_url_rule('/listarAtributosResultado/',
                 view_func=ListarAtributosResultado.as_view('listarAtributosResultado'),
                 methods=["GET"])

app.add_url_rule('/modificarItem/',
                 view_func=ModificarItem.as_view('modificarItem'),
                 methods=["POST"])


app.add_url_rule('/eliminarRevivirAprobarItem/',
                 view_func=EliminarRevivirAprobarItem.as_view('eliminarRevivirAprobarItem'),
                 methods=["POST"])

app.add_url_rule('/listarDatosItemVersion/',
                 view_func=ListarDatosItemVersion.as_view('listarDatosItemVersion'),
                 methods=["GET"])

app.add_url_rule('/itemsRelacionarMiniDialogoComboBox/',
                 view_func=ListarItemsRelacionarMiniDialogoComboBox.as_view('listarItemsRelacionarMiniDialogoComboBox'),
                 methods=["GET"])

app.add_url_rule('/agregarRelacion/',
                 view_func=AgregarRelacion.as_view('agregarRelacion'),
                 methods=["POST"])

app.add_url_rule('/listarRelaciones/',
                 view_func=ListarRelaciones.as_view('listarRelaciones'),
                 methods=["GET"])

app.add_url_rule('/eliminarRelacion/',
                 view_func=EliminarRelacion.as_view('eliminarRelacion'),
                 methods=["POST"])

app.add_url_rule('/adjuntarArchivo/',
                 view_func=AdjuntarArchivo.as_view('adjuntarArchivo'),
                 methods=["GET","POST"])



app.add_url_rule('/LBManager/',
                 view_func=LBManager.as_view('LBManager'),
                 methods=["GET","POST"])
app.add_url_rule('/agregarLB/',
                 view_func=AgregarLB.as_view('agregarLB'),
                 methods=["GET","POST"])
app.add_url_rule('/modificarLB/',
                 view_func=ModificarLB.as_view('modificarLB'),
                 methods=["GET","POST"])
app.add_url_rule('/listarLB/',
                 view_func=ListarLB.as_view('listarLB'),
                 methods=["GET","POST"])
app.add_url_rule('/listarItemBase/',
                 view_func=ListarItemBase.as_view('listarItemBase'),
                 methods=["GET","POST"])
app.add_url_rule('/agregarItemLB/',
                 view_func=AgregarItemLB.as_view('agregarItemLB'),
                 methods=["GET","POST"])
app.add_url_rule('/cerrarLB/',
                 view_func=CerrarLB.as_view('cerrarLB'),
                 methods=["GET","POST"])




app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0')