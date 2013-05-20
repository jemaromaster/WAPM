import flask
import flask.views
from utils import login_required
from models.usuarioModelo import Usuario 
from models.bdCreator import Session
from UsuarioController import UsuarioControllerClass

class ModificarUsuario(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def get(self):
        """
        prueba
        """
        return "nada"
    
    @login_required
    def post(self):
        """
        prueba
        """ 
        uc=UsuarioControllerClass()
        idUsuario=flask.request.form['idUsuario'] 
        print "id usuario es :  " + idUsuario
        if 'passNuevo' in flask.request.form:
            passNuevo=flask.request.form['passNuevo']
            return  uc.controlarPass(passNuevo,idUsuario)
        
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
        '''
        sesion=Session()
        
        #eSssion.query(MyClass).filter(MyClass.name == 'some name')
        
        u=sesion.query(Usuario).filter(Usuario.id==idUsuario).first()
        u.setValues(nombreUsuario,passwd, nombre, apellido,email,ci,telefono,observacion,activo,direccion)
        sesion.commit()
        sesion.close()'''
        
        u=Usuario(nombreUsuario,passwd, nombre, apellido,email,ci,telefono,observacion,activo,direccion)
        
        return uc.controlarUsuario(u, idUsuario)
        