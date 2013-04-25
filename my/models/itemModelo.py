from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from bdCreator import Base
import flask.views
class Item(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de Items
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: 
    nombre, versión, prioridad, tipo de item, 
    fecha de inicio, fecha de finalización, 
    complejidad, tiempo estimado,estado, descripción, 
    archivos externos, fecha creación, ultima modificación, autorVersion
    """
    #Nombre de la tabla
    __tablename__ = 'item'
    
    #Columnas
    idModelo = Column("id",Integer, primary_key=True)
    nombreItem =  Column("nombre",String(20))
    version=Column("version",Integer)
    prioridad=Column("prioridad",Integer)
    fechaInicio=Column("fecha_inicio", Date)
    fechaFinalizacion=Column("fecha_finalizacion", Date)
    #tipoItem=relationship('Usuario',
    #                              secondary=miembrosProyectoTabla,
    #                              backref='proyectos')
    complejidad=Column("complejidad", Integer)
    #tiempoEstimado=
    estado=Column("estado", String(12))
    descripcion=Column("descripcion", String(50))
    #archivoExterno
    fechaCreacion= Column("nombre",Date)
    ultimaModificacion= Column("nombre",TIMESTAMP)
    autorVersion= relationship('Usuario',
                                 secondary=miembrosProyectoTabla,
                                 backref='proyectos')
    
    idProyecto = Column(Integer, ForeignKey('PROYECTO.id_proyecto'))
    #item=
    '''para obtener el one to many desde proyecto (un proyecto, muchas fases se utiliza una foreignkey 
    como en este caso mas arriba idProyecto
    '''
    def setValues(self,nombreFase, descripcion, estado, fechaInicio, fechaFinalizacion, idProyecto):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: id, nombre, descripcion, estado
        """
              
        self.nombreFase=nombreFase; 
        self.descripcion=descripcion;
        self.estado=estado;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.idProyecto=idProyecto;
        
    def __init__(self,nombreFase, descripcion, estado, fechaInicio, fechaFinalizacion, idProyecto):
        """
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: id, nombre, descripcion, estado
        """
        self.nombreFase=nombreFase; 
        self.descripcion=descripcion;
        self.estado=estado;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.idProyecto=idProyecto;
        