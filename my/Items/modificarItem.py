import flask, json, datetime
import flask.views
from utils import login_required
from models.itemModelo import Item
from itemController import ItemControllerClass
from models.bdCreator import Session

class ModificarItem(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de modificacion de 
    usuario al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    
    @login_required
    def get(self):
        """
        prueba
        """
        return "nada"
    
    @login_required
    def post(self):
        
        atributos=json.loads(flask.request.form['atributos'])
        idItem=flask.request.form['idItem']
        nombreItem=flask.request.form['nombreItem']
        prioridad=flask.request.form['prioridad']
        fechaInicio=flask.request.form['fechaInicio']
        fechaFinalizacion=flask.request.form['fechaFinal']
        tipoItemId=0; #aca le paso 0 ya que el tipo item no cambia y es el mismo de la version anterior
        complejidad=flask.request.form['complejidad']
        costo=flask.request.form['costo']
        estado=flask.request.form['estado']
        descripcion=flask.request.form['descripcion']
        fechaCreacion= datetime.date.today()
        #este autorVersion se extrae del idUsuario de la sesion
        autorVersion_id=flask.session['idUsuario']
        
        idFase=flask.request.form['idFase']
       
        fechaInicio=fechaInicio[3:5]+'/'+fechaInicio[0:2]+'/'+fechaInicio[6:10]
        fechaFinalizacion=fechaFinalizacion[3:5]+'/'+fechaFinalizacion[0:2]+'/'+fechaFinalizacion[6:10]
        #ver fechaCreacion TIMESTAMP
       
        i=Item(nombreItem, prioridad, costo, complejidad, fechaInicio, \
               fechaFinalizacion, tipoItemId, estado, descripcion,\
                  fechaCreacion, autorVersion_id, idFase)
        

        ic=ItemControllerClass()
        
        
        return ic.controlarItem(i, idItem, atributos)
    