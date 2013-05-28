from models.lineaBaseModelo import LineaBase  
from models.bdCreator import Session
from flask import make_response

class LBManejador:
    """
    Clase que es utilizada para guardar los datos de una linea base una vez que sus datos han sido 
    controlados. 
    """
    def guardarLB(self, lb, idLb):
        """
        Metodo utilizado para guardar los datos de la fase
        @type  lb: LineaBase
        @param lb: LineaBase cuyos datos seran controlados antes de ser almacenados en la bd
        @type  idLb: number
        @param idLb: El id de la LineaBase. Si es cero, la LineaBase enviada es nueva, sino, es una
            LineaBase ya existente cuyos atributos quieren ser modificados.
        """
        sesion=Session()
        l=lb
        if idLb != 0:
            l=sesion.query(LineaBase).filter(LineaBase.id==idLb).first()
            l.descripcion=lb.descripcion;l.estado=lb.estado
            
            
        sesion.add(l)
        sesion.commit()
        sesion.close()
        
        return make_response("f,LineaBase guardada correctamente!")
        
