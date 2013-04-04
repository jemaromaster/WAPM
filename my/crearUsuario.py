import flask
from utils import login_required
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#from models.db_def import engine


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
        nombre=flask.request.form['nombre']
        apellido= flask.request.form['apellido']
        email=flask.request.form['email']
        
        if passwd!=repPasswd:
            flask.flash("Las contrasenhas no coinciden")
            return flask.redirect(flask.url_for('crearUsuario'))
        #guardar
        
        
               
   