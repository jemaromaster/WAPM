import flask.views
from utils import login_required
from models.proyectoModelo import Proyecto
from models.faseModelo import Fase

from models.bdCreator import Session

class FinalizarProyecto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de activacion de 
    proyecto al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    def post(self):
    
        idProyecto=flask.request.form['idProyecto']
        idProyecto=idProyecto.strip()
        if idProyecto=="0" or idProyecto=='':
            return "t, Fase no valida"
         
        sesion=Session()
        proyecto= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).first()
        
        #Controles
        if proyecto is None:
            return "t,La El proyecto no existe"
        
        if proyecto.estado != "activo":
            return "t,No se puede finalizar un proyecto que no este activo!"
        
        fasesProyecto= sesion.query(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idProyecto))
        
        for fase in fasesProyecto:
            if fase.estado!="finalizada":
                return "t,Todas las FASES deben estar FINALIZADAS"
            
        proyecto.estado="finalizado"
        sesion.add(proyecto)
        sesion.commit()
        sesion.close()
        
        return "f,Ha finalizado el proyecto!" 
    
        
            
