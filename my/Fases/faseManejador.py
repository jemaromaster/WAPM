from models.faseModelo import Fase
from models.bdCreator import Session
from flask import make_response


class FaseManejador:
    def guardarFase(self, fase, idFase):
        sesion=Session()
        f=fase;
        
        if(idFase!=0): 
            f=sesion.query(Fase).filter(Fase.idFase==idFase).first()
            f.setValues(fase.nombreFase,fase.descripcion, \
                        fase.estado, fase.fechaInicio,\
                        fase.fechaFinalizacion,\
                        fase.idProyecto)
        
        sesion.add(f)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Fase guardada correctamente")
        
