from flask import views, make_response
import flask.views
from models.lineaBaseModelo import LineaBase 
from models.bdCreator import Session

from LBManejador import LBManejador

class LBControllerClass(flask.views.MethodView):
    """
    Clase que es utilizada para controlar los datos recibidos del cliente,
    para asegurarse de que no se almacenen valores inconsistentes en la bd 
    
    """
    def controlarLB(self,lb,idLb):
        """
        Metodo utilizado para controlar los datos recibidos del cliente
        @type  lb: LineaBase
        @param lb: LineaBase cuyos datos seran controlados antes de ser almacenados en la bd
        @type  idLb: number
        @param idLb: El id de la linea base. Si es cero, la linea base enviada es nueva, sino, es una
            linea base ya existente cuyos atributos quieren ser modificados.
        """
        if len(lb.estado) <= 0 or len(lb.estado) > 15:
            return make_response("f,Estado de LineaBase incorrecto")
        if len(lb.descripcion) <= 0 or len(lb.descripcion) > 50:
            return make_response("f,Descripcion de LineaBase incorrecto")
        
        sesion=Session()
        controlDesc=sesion.query(LineaBase).filter(LineaBase.descripcion==lb.descripcion).first()
        if idLb==0:    
            if controlDesc is not None:
                sesion.close()
                return make_response("t,Descripcion de LineaBase coincide con otra!")
            if lb.idFase == '' or lb.idFase=='0':
                sesion.close()
                return make_response("t,Fase no valida. No se pudo crear la LineaBase")
            lb.idFase=int(lb.idFase)
        else:
            
            if controlDesc is not None and controlDesc.id != int(idLb):
                sesion.close()
                return make_response("t,Descripcion de LineaBase coincide con otra!")    
        lbm=LBManejador()    
        sesion.close()
        return lbm.guardarLB(lb, idLb)
            