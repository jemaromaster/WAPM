from models.usuarioModelo import Usuario 
from models.bdCreator import Session
from flask import make_response

class UsuarioManejador:
    def guardarUsuario(self, user):
        
        u=user;
        sesion=Session()
        sesion.add(u)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Usuario guardado correctamente")
        
