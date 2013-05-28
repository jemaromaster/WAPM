import flask.views
from utils import login_required
from models.itemModelo import Item
from models.faseModelo import Fase

from models.bdCreator import Session

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
        
        itemsFase= sesion.query(Item).join(Fase).filter(Fase.idFase==int(idFase))
        
        numberItems=itemsFase.count() 
        if numberItems <= 0:
            sesion.close()
            return "t,La fase no posee items!"
        
        for item in itemsFase:
            if item.estado!="bloqueado":
                sesion.close()
                return "t,Todos los ITEMS deben estar BLQUEADOS"
            
        fase.estado="finalizada"
        sesion.add(fase)
        sesion.commit()
        sesion.close()
        
        return "f,La fase ha sido finalizada!" 
    
        
            
