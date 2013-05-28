from models.faseModelo import Fase
from models.bdCreator import Session
from flask import make_response


class FaseManejador:
    """
    Clase que es utilizada para guardar los datos de una fase una vez que sus datos han sido 
    controlados. 
    """
    def guardarFase(self, fase, idFase):
        """
        Metodo utilizado para guardar los datos de la fase
        @type  f: Fase
        @param f: Fase cuyos datos seran controlados antes de ser almacenados en la bd
        @type  idF: number
        @param idF: El id de la fase. Si es cero, la fase enviada es nueva, sino, es una
            fase ya existente cuyos atributos quieren ser modificados.
        """
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
        
