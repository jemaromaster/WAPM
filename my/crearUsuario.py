import flask
from utils import login_required
from models.usuarioModelo import Usuario 
from models.bdCreator import Session

class CrearUsuario(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
        required=['nombreUsuario','pass', 'repPass','nombre','apellido','email']
        for r in required:
            if r not in flask.request.form:
                flask.flash("No se completo campos obligatorios ")
                return flask.redirect(flask.url_for('crearUsuario'))
        
        nombreUsuario=flask.request.form['nombreUsuario']
        passwd=flask.request.form['pass']
        repPasswd=flask.request.form['repPass']
        ci=flask.request.form['ci']
        nombre=flask.request.form['nombre']
        apellido= flask.request.form['apellido']
        email=flask.request.form['email']
        direccion=flask.request.form['direccion']
        telefono=flask.request.form['telefono']
        observacion=flask.request.form['observacion']
        u=Usuario(nombreUsuario,passwd, nombre, apellido,email,ci,telefono,observacion)
        if passwd!=repPasswd:
            flask.flash("Las contrasenhas no coinciden")
            return flask.redirect(flask.url_for('crearUsuario'))
        else:
            sesion=Session()
            sesion.add(u)
            sesion.commit()
            sesion.close()
            return flask.redirect(flask.url_for('usuarioManager'))
            
        
        
               
   