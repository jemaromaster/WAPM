import flask.views
from utils import login_required
from utils import rolPL_required
from models.proyectoModelo import Proyecto
from models.faseModelo import Fase
from models.bdCreator import Session

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
            return "t,El proyecto no existe"
        
        if proyecto.estado != "desarrollo":
            return "t,No se puede pasar a Activo, el proyecto debe estar en desarrollo!"
        
        numberMiembros= len(proyecto.usuariosMiembros)
        if numberMiembros <= 0:
            return "t,El proyecto no posee miembros!"
            
        numberComite= len(proyecto.usuariosComite)
        if numberComite  <= 0:
            return "t,El comite de cambios no posee miembros!"
        resto= numberComite % 2
        if resto == 0:
            return "t,El comite de cambios debe estar compuesto por un numero impar de miembros!"
        
        numberFases= sesion.query(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).join(Fase).count();
        if numberFases <= 0:
            return "t,No se puede pasar a Activo, el proyecto no contiene fases!"
        
        proyecto.estado="activo"
        sesion.add(proyecto)
        sesion.commit()
        
        
        sesion.close()
        
        return "f,El proyecto ha sido activado! Ya no se permitiran modificaciones." 
    
        
            