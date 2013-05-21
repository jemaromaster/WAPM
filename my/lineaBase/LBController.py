from flask import views, make_response
import flask.views
from models.lineaBaseModelo import LineaBase 
from models.bdCreator import Session

from LBManejador import LBManejador

class LBControllerClass(flask.views.MethodView):
    
    def controlarLB(self,lb,idLb):
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
            