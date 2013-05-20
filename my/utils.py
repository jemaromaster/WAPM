import flask, functools 

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("Se necesita iniciar sesion!")
            return flask.redirect(flask.url_for('index'))
    return wrapper

def rolPL_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'rolPL' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("No es project leader!")
            return flask.redirect(flask.url_for('index'))
    return wrapper

def rolAdmin_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'rolAdmin' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("No es Administrador!")
            return flask.redirect(flask.url_for('index'))
    return wrapper