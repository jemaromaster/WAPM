from models.lineaBaseModelo import LineaBase  
from models.bdCreator import Session
from flask import make_response

class LBManejador:
    def guardarLB(self, lb, idLb):
        sesion=Session()
        l=lb
        if idLb != 0:
            l=sesion.query(LineaBase).filter(LineaBase.id==idLb).first()
            l.descripcion=lb.descripcion;l.estado=lb.estado
            
            
        sesion.add(l)
        sesion.commit()
        sesion.close()
        
        return make_response("f,LineaBase guardada correctamente!")
        
