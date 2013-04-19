import flask
from flask import views,make_response
from models.bdCreator import Session
from models.usuarioModelo import Usuario
sesion=Session()

class Login(flask.views.MethodView):
    """
    Clase utilizada para la verificacion de identiad del usuario. Recibe 
    el usuername y contrasenha, si dicho par existe en la base de datos
    del sistema, se concede el acceso
    """
    def get(self):
        if 'username' in flask.session:
            return flask.render_template('usuarioManager.html')
        return flask.render_template('index.html')
    
    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        
        c=sesion.query(Usuario).filter(Usuario.username==username).filter(Usuario.passwd==passwd).count()
        usuarioSesion=sesion.query(Usuario).filter(Usuario.username==username).filter(Usuario.passwd==passwd).first()
        if usuarioSesion == None:
            responde=make_response("t,Usuario no existe o el passaword es incorrecto")
            return responde
        idUsuarioSession=usuarioSesion.id;
        
        if c==1:
            flask.session['username'] = username
            flask.session['idUsuario']= idUsuarioSession
        else:
            responde=make_response("t,Usuario no existe o el passaword es incorrecto")   
            return responde
        return flask.redirect(flask.url_for('usuarioManager'))
        #return flask.render_template('usuarioManager.html')