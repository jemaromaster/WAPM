from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from faseModelo import Fase
#from usuarioModelo import Usuario
class Item(Base):
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
    
    '''para obtener el one to many desde proyecto (un proyecto, muchas fases se utiliza una foreignkey 
    como en este caso mas arriba idProyecto
    '''
    def setValues(self,nombreItem, prioridad, costo, complejidad,fechaInicio, \
                  fechaFinalizacion, tipoItem_id, estado, descripcion, \
                  fechaCreacion, autorVersion_id, idFase):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: id, nombre, descripcion, estado
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
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: id, nombre, descripcion, estado
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
        