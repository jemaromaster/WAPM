from models.usuarioModelo import Usuario 
from models.bdCreator import Session
from flask import make_response

class UsuarioManejador:
    def guardarUsuario(self, user, idUsuario):
        sesion=Session()
        u=user;
        if(idUsuario!=0):
            u=sesion.query(Usuario).filter(Usuario.id==idUsuario).first()
            u.setValues(user.username,user.passwd, user.nombres, user.apellidos,\
                        user.email,user.ci,user.telefono,user.observacion,user.activo,\
                        user.direccion)
        
      
        sesion.add(u)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Usuario guardado correctamente")
        
