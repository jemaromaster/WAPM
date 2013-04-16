from flask import views, make_response
import flask.views

from models.usuarioModelo import Usuario 
from models.bdCreator import Session

from usuarioManejador import UsuarioManejador

class UsuarioControllerClass(flask.views.MethodView):
    def controlarUsuario(self, usuario):
        u=usuario
        
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
        
        '''controla el tamano de los strings'''
         
        if not(1<=len(u.username)<20 and 1<=len(u.passwd)<20 \
              and 1<=len(u.nombres)<30 and 1<=len(u.apellidos)<30 and 1<=len(u.email)<30 \
              and 1<=len(u.ci)<10and 0<=len(u.telefono)<13 and 0<=len(u.observacion)<50 \
              and 1<=len(u.activo)<10 and 0<=len(u.direccion)<30): 
            return make_response('t,Se supera caracteres de los campos ')
            
        
        '''controla caracteres validos en el username'''
        
        for r in u.username:
            if not(65<=ord(r)<=90 or 48<=ord(r)<=57 or 97<=ord(r)<=122):
                responde=make_response("t,El username tiene espacios")
                return responde
        print "controla"
        
        '''consulta si es que existe ya usuario con ese nombre'''
        
        sesion=Session()
        usr=sesion.query(Usuario).filter(Usuario.username==u.username).first()
        if(usr is not None):
            return make_response('t,Ya existe el usuario')
        
        um=UsuarioManejador()
        
        return um.guardarUsuario(u)
        