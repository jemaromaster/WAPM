
import flask.views
from utils import login_required
from models.usuarioModelo import Usuario
from Usuarios.UsuarioController import UsuarioControllerClass;
from models.bdCreator import Session
from models.rolSistemaModelo import RolSistema
import json


class AgregarUsuario(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de creacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def get(self):
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
        rolSistemaJSON=flask.request.form['rolSistema']
        nombreUsuario=flask.request.form['nombreUsuario']
        passwd=flask.request.form['password']
        ci=flask.request.form['ci']
        nombre=flask.request.form['nombre']
        apellido= flask.request.form['apellido']
        email=flask.request.form['email']
        direccion=flask.request.form['direccion']
        telefono=flask.request.form['telefono']
        observacion=flask.request.form['observacion']
        activo=flask.request.form['activo']

        sesion=Session()
        rolSistema=json.loads(rolSistemaJSON)
        print "rol de sistema para project leader! "+ rolSistema[0]
        print "rol de sistema para administrador de usuarios! "+ rolSistema[1]
        rs=[]
        if rolSistema[0]=="1":
            rolSis=sesion.query(RolSistema).filter(RolSistema.nombre=="Project Leader").first()
            rs.append(rolSis)
        if rolSistema[1]=="1":
            rolSis=sesion.query(RolSistema).filter(RolSistema.nombre=="Administrador").first()
            rs.append(rolSis)
        sesion.close()    
        u=Usuario(nombreUsuario,passwd, nombre, apellido,email,ci,telefono,observacion,activo,direccion)
       
        u.username=u.username.strip()
        u.nombres=u.nombres.strip()
        u.passwd=u.passwd.strip()
        u.apellidos=u.apellidos.strip()
        u.email=u.email.strip()
        u.ci=u.ci.strip()
        u.telefono=u.telefono.strip()
        u.observacion=u.observacion.strip()
        u.activo=u.activo.strip()
        u.direccion=u.direccion.strip()
        for roles in rs:
            u.roles_sistema.append(roles)
      
        uc=UsuarioControllerClass()
        
        return uc.controlarUsuario(u, 0)
    
        
            
        
        
               
