import flask.views
from utils import login_required
from utils import rolPL_required
from models.proyectoModelo import Proyecto
from models.faseModelo import Fase
from models.bdCreator import Session
import datetime

class ActivarProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de activacion de 
    proyecto al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    @rolPL_required
    def post(self):
    
        idProyecto=flask.request.form['idProyecto']
        sesion=Session()
        
        proyecto= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
        
        #Controles
        if proyecto is None:
            sesion.close()
            return "t,El proyecto no existe"
        
        if proyecto.estado != "desarrollo":
            sesion.close()
            return "t,No se puede pasar a Activo, el proyecto debe estar en desarrollo!"
        
        numberMiembros= len(proyecto.usuariosMiembros)
        if numberMiembros <= 0:
            sesion.close()
            return "t,El proyecto no posee miembros!"
            
        numberComite= len(proyecto.usuariosComite)
        if numberComite  <= 0:
            sesion.close()
            return "t,El comite de cambios no posee miembros!"
        resto= numberComite % 2
        if resto == 0:
            sesion.close()
            return "t,El comite de cambios debe estar compuesto por un numero impar de miembros!"
        
        numberFases= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).join(Fase).count();
        if numberFases <= 0:
            sesion.close()
            return "t,No se puede pasar a Activo, el proyecto no contiene fases!"
        
        fasesProyecto=sesion.query(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idProyecto));
        for fase in fasesProyecto:
            fase.estado="activa"
            print "Fase:  "+fase.nombreFase+" estado de la fase: "+fase.estado
            sesion.add(fase)
            
        now=datetime.date.today()
        proyecto.fechaInicio=now
        proyecto.estado="activo"
        
        primeraFase=sesion.query(Fase).filter(Fase.idProyecto==idProyecto,Fase.tag=="F1").first()
        primeraFase.fechaInicio=proyecto.fechaInicio
        sesion.add(proyecto)
        sesion.add(primeraFase)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,El proyecto ha sido activado! Ya no se permitiran modificaciones." 
    
        
            
