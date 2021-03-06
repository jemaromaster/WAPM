import flask, functools 
from models.bdCreator import Session
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario


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

def miembroComite_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        
        sesion=Session()
        idProyectoSeleccion=flask.session['idProyecto']
        idUsuario=flask.session['idUsuario']
        comiteProject=sesion.query(Usuario.id).filter(Proyecto.idProyecto==idProyectoSeleccion).join(Proyecto.usuariosComite)\
                                          .filter(Usuario.id==idUsuario).first();

        if comiteProject is None:
            sesion.close()
            if 'rolPL' in flask.session or'rolAdmin' in flask.session:
                return flask.redirect(flask.url_for('miembros'))
            flask.flash("No es miembro del comite!")
            return flask.redirect(flask.url_for('index'))                                   
        else:
            print "PARTE DEL COMITE!!   "
            sesion.close()
            return method(*args, **kwargs)
    return wrapper


def controlRol(idFase,componente,permiso):
    
    permisos=flask.session['permisos']
    idUsuario=flask.session['idUsuario']
    idProyecto=flask.session['idProyecto']
    
    sesion=Session()
    idPL=sesion.query(Proyecto.projectLeaderId).filter(Proyecto.idProyecto==int(idProyecto)).first()
    print "id project  leader es:  "+str(idPL.projectLeaderId)+"id del usuario logueado es "+str(idUsuario)
    if idPL.projectLeaderId==int(idUsuario):
        sesion.close()
        return 1
    respuesta=0
    print "a veeeeeeeeer la fase que envio    " + idFase
    for p in permisos:
        '''corrobora si existe el permiso(consultar,finalizar,administrar) sobre el componente (fase,lb,item,tipo)'''
        
        if idFase in permisos:
            
            if permisos[idFase][componente][permiso]==1:
                respuesta=1
                sesion.close()
                return respuesta
    sesion.close()        
    return respuesta
