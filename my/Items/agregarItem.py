import flask.views
from utils import login_required,controlRol
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item


class AgregarItem(flask.views.MethodView):
    """Clase utilizada cuando se hace una peticion de creacion de 
    Item al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo """
    
    @login_required
    def get(self):
        return flask.render_template('crearUsuario.html')
    
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos con los que se creara un nuevo item dentro
        de algun proyecto y fase determinada. 
        @type  atributos: JSON_ATRIBUTOS
        @param atributos: atributos dinamicos dependientes del tipo de item
        @type  nombreItem: string
        @param nombreItem: nombre del item 
        @type fechaInicio: date 
        @param fechaInicio: fecha de inicio 
        @type  fechaFinal: date
        @param fechaFinal: fecha de finalizacion 
        @type  descripcion: String
        @param descripcion: una descripcion del item
        @type prioridad: int
        @param prioridad: prioridad a darle al item
        @type complejidad: int
        @param complejidad: complejidad del item entre [0.20]
        @type  idFase: String
        @param idFase: el id de la fase al cual la fase pertenecera
        @type estado: String
        @param estado: define el estado del item activo, inactivo, bloqueado, desarrollo, pendiente 
        """
        atributos=json.loads(flask.request.form['atributos'])
        nombreItem=flask.request.form['nombreItem']
        prioridad=flask.request.form['prioridad']
        fechaInicio=flask.request.form['fechaInicio']
        fechaFinalizacion=flask.request.form['fechaFinal']
        tipoItemId=flask.request.form['tipoItemId']
        complejidad=flask.request.form['complejidad']
        costo=flask.request.form['costo']
        estado=flask.request.form['estado']
        descripcion=flask.request.form['descripcion']
        
        fechaCreacion= datetime.date.today()
        print(fechaCreacion)
        #este autorVersion se extrae del idUsuario de la sesion
        autorVersion_id=flask.session['idUsuario']
        
        idFase=flask.request.form['idFase']
        '''
        fechaInicio=fechaInicio[3:5]+'/'+fechaInicio[0:2]+'/'+fechaInicio[6:10]
        fechaFinalizacion=fechaFinalizacion[3:5]+'/'+fechaFinalizacion[0:2]+'/'+fechaFinalizacion[6:10]
        '''
        #ver fechaCreacion TIMESTAMP
        if controlRol(str(idFase),'item','administrar')==0:
                return "t, No tiene permisos para realizar esta accion"
        i=Item(nombreItem, prioridad, costo, complejidad, fechaInicio, \
               fechaFinalizacion, tipoItemId, estado, descripcion,\
                  fechaCreacion, autorVersion_id, idFase)
        

        ic=ItemControllerClass()
        
        
        return ic.controlarItem(i, 0, atributos, 0)
    
        
            
        
        
               
