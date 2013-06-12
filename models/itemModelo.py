from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from faseModelo import Fase
#from usuarioModelo import Usuario

class Relacion(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de relacion
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__='relacion'
    idRelacion=Column("id",Integer, primary_key=True)
    padre_id = Column(Integer, ForeignKey('item.id'))
    hijo_id = Column(Integer, ForeignKey('item.id'))
    versionHijo=Column("version_hijo",Integer)
    
    padres=relationship("Item", primaryjoin="Relacion.padre_id==Item.idItem")
    hijos=relationship("Item", primaryjoin="Relacion.hijo_id==Item.idItem")
    
    def setValues (self, padre_id, hijo_id, versionHijo):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type padre_id : Integer
        @param padre_id : id del item padre
        @type versionHijo : Integer
        @param versionHijo : numero de version del hijo
        @type hijo_id : Integer
        @param hijo_id : id del item hijo
        """
        self.padre_id=padre_id;
        self.hijo_id=hijo_id;
        self.versionHijo=versionHijo;
    
    def __init__(self, padre_id, hijo_id, versionHijo):
        """
        Constructor de la clase 
        @type padre_id : Integer
        @param padre_id : id del item padre
        @type versionHijo : Integer
        @param versionHijo : numero de version del hijo
        @type hijo_id : Integer
        @param hijo_id : id del item hijo
        """
        self.padre_id=padre_id;
        self.hijo_id=hijo_id;
        self.versionHijo=versionHijo;
class Item(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de item
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    #Nombre de la tabla
    __tablename__ = 'item'
    
    #Columnas
    idItem = Column("id",Integer, primary_key=True)
    nombreItem =  Column("nombre",String(20))
    version=Column("version",Integer)
    prioridad=Column("prioridad",Integer)
    costo=Column("costo",Integer)
    complejidad=Column("complejidad",Integer)
    fechaInicio=Column("fecha_inicio", Date)
    fechaFinalizacion=Column("fecha_finalizacion", Date)
    
    #MANY TO ONE
    tipoItem=relationship('TipoItem', backref='items')
    tipoItem_id= Column(Integer, ForeignKey('tipo_item.id'))
    
    estado=Column("estado", String(12))
    descripcion=Column("descripcion", String(50))
    #archivoExterno
    fechaCreacion= Column("fecha_creacion",TIMESTAMP)
   
    
    #MANY TO ONE
    autorVersion= relationship('Usuario',backref='item')
    autorVersion_id=Column(Integer, ForeignKey('usuario.id'))
    idFase= Column(Integer, ForeignKey('fase.id'))
    fases= relationship("Fase", backref="items")
    
    tag=Column("tag", String(30))
    
    '''para obtener el one to many desde proyecto (un proyecto, muchas fases se utiliza una foreignkey 
    como en este caso mas arriba idProyecto
    '''
    def setValues(self,nombreItem, prioridad, costo, complejidad,fechaInicio, \
                  fechaFinalizacion, tipoItem_id, estado, descripcion, \
                  fechaCreacion, autorVersion_id, idFase):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type nombreItem : string
        @param nombreItem : nombre del item
        @type prioridad : Integer
        @param prioridad : Prioridad del item
        @type costo : Integer
        @param costo : Costo economico asociado al item
        @type complejidad : Integer
        @param complejidad : Costo de complejidad asociado al item
        @type fechaInicio : Date
        @param fechaInicio : fecha de inicio del item
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion del item
        @type tipoItem_id : Integer
        @param tipoItem_id : id correspondiente al tipo de item del cual se instancion el item
        @type estado : String
        @param estado : descripcion del estado en que se encuentra el item
        @type descripcion : String
        @param descripcion : descripcion del item
        @type fechaCreacion : Date
        @param fechaCreacion : fecha en que se creo el item
        @type autoVersion_id : Integer
        @param autoVersion_id : auto version
        @type idFase : Integer
        @param idFase : Fase a la cual esta relacionada este Item
        """
              
        self.nombreItem=nombreItem;
        self.prioridad=prioridad;
        self.tipoItem_id=tipoItem_id;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.estado=estado;
        self.descripcion=descripcion;
        self.fechaCreacion=fechaCreacion;
        self.autorVersion_id=autorVersion_id;
        self.idFase=idFase;
        
        self.costo=costo;
        self.complejidad=complejidad;
        
    def __init__(self,nombreItem, prioridad, costo, complejidad,fechaInicio, \
                  fechaFinalizacion, tipoItem_id,estado, descripcion, \
                  fechaCreacion, autorVersion_id, idFase):
        """
        Constructor de la clase 
        @type nombreItem : string
        @param nombreItem : nombre del item
        @type prioridad : Integer
        @param prioridad : Prioridad del item
        @type costo : Integer
        @param costo : Costo economico asociado al item
        @type complejidad : Integer
        @param complejidad : Costo de complejidad asociado al item
        @type fechaInicio : Date
        @param fechaInicio : fecha de inicio del item
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion del item
        @type tipoItem_id : Integer
        @param tipoItem_id : id correspondiente al tipo de item del cual se instancion el item
        @type estado : String
        @param estado : descripcion del estado en que se encuentra el item
        @type descripcion : String
        @param descripcion : descripcion del item
        @type fechaCreacion : Date
        @param fechaCreacion : fecha en que se creo el item
        @type autoVersion_id : Integer
        @param autoVersion_id : auto version
        @type idFase : Integer
        @param idFase : Fase a la cual esta relacionada este Item
        """
        
        
        self.nombreItem=nombreItem;
        self.prioridad=prioridad;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.tipoItem_id=tipoItem_id;
        self.estado=estado;
        self.descripcion=descripcion;
        self.fechaCreacion=fechaCreacion;
        self.autorVersion_id=autorVersion_id;
        self.idFase=idFase;
        
        
        self.costo=costo;
        self.complejidad=complejidad;
        