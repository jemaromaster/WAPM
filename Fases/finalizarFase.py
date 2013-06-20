import flask.views
from utils import login_required
from utils import controlRol
from models.itemModelo import Item
from models.faseModelo import Fase
from models.lineaBaseModelo import LineaBase
from models.proyectoModelo import Proyecto
from models.bdCreator import Session
import datetime
class FinalizarFase(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de finalizacion de 
    fase al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos de la fase que sera finalizada
        dentro del proyecto.
        @type idFase : String
        @param idFase : Id de la fase a la cual se le cambiara el estado por finalizado
        """
        idFase=flask.request.form['idFase']
        if controlRol(idFase,'fase','finalizar')==0:
            return "t, No posee permiso para esta accion"
        
        idFase=idFase.strip()
        if idFase=="0" or idFase=='':
            return "t, Fase no valida"
         
        sesion=Session()
        fase= sesion.query(Fase).filter(Fase.idFase==int(idFase)).first()
        
        #Controles
        if fase is None:
            sesion.close()
            return "t,La fase no existe"
        
        if fase.estado != "activa":
            sesion.close()
            return "t,No se puede finalizar una fase que no este activa"
        
        #Controla items en la fase
        itemsFase= sesion.query(Item).join(Fase).filter(Fase.idFase==int(idFase))
        
        numberItems=itemsFase.count() 
        if numberItems <= 0:
            sesion.close()
            return "t,La fase no posee items!"
        
        for item in itemsFase:
            if item.estado!="bloqueado":
                sesion.close()
                return "t,Todos los ITEMS deben estar BLQUEADOS"
        
        #Controla LBs en la fase
        bases= sesion.query(LineaBase).join(Fase).filter(Fase.idFase==int(idFase),LineaBase.estado=="cerrada").count()
        if bases <= 0:
                sesion.close()
                return "t,Todas las Lineas Bases deben estar Cerradas"
        #Controla que todas las fases anteriores esten finalizadas
        idProyecto= fase.idProyecto
        fases=sesion.query(Fase).join(Proyecto).filter(Proyecto.idProyecto==idProyecto).all()
        for f in fases:
            if f.idFase < fase.idFase:
                if f.estado!="finalizada":
                    sesion.close()
                    return "t,Fases anteriores deben ser finalizadas primeramente!"
        for f in fases:
            if f.idFase > fase.idFase:
                f.estado="activa"
                f.fechaFinalizacion=None
                sesion.add(f)
        fase.estado="finalizada"
        now=datetime.date.today()
        fase.fechaFinalizacion=now
        #Pone como fecha de inicio de fase sgte la fecha de finalizacion de la actual
        tagFaseSgte="F"+str(int(fase.tag[1:])+1)
        faseSgte=sesion.query(Fase).join(Proyecto).filter(Proyecto.idProyecto==idProyecto)\
                                                    .filter(Fase.tag==tagFaseSgte).first()
        if faseSgte != None:
            faseSgte.fechaInicio=fase.fechaFinalizacion
            sesion.add(faseSgte)                                            
        
        sesion.add(fase)
        sesion.commit()
        sesion.close()
        
        return "f,La fase ha sido finalizada!" 
    
        
            
