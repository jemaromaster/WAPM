
import flask.views
from utils import login_required
from models.usuarioModelo import Usuario
from UsuarioController import UsuarioControllerClass;



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
        
        u=Usuario(nombreUsuario,passwd, nombre, apellido,email,ci,telefono,observacion,activo,direccion)
        
        # cu=UsuarioControllerClass()
        #retorno=cu.controlarUsuario(u)
        
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
        
      
        
        uc=UsuarioControllerClass()
        
        return uc.controlarUsuario(u)
    
        
            
        
        
               
