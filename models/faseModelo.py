from sqlalchemy import Column, Integer, String, Date, ForeignKey
from bdCreator import Base
import flask.views
class Fase(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de Fases
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    #Nombre de la tabla
    __tablename__ = 'fase'
    
    #Columnas
    idFase = Column("id",Integer, primary_key=True)
    nombreFase =  Column("nombre",String(20))
    descripcion=Column("descripcion",String(50))
    estado=Column("estado", String(12))
    fechaInicio=Column("fecha_inicio", Date)
    fechaFinalizacion=Column("fecha_finalizacion", Date)
    idProyecto = Column(Integer, ForeignKey('proyecto.id_proyecto'))
    tag=Column("tag",String(10))
    #item=
    '''para obtener el one to many desde proyecto (un proyecto, muchas fases se utiliza una foreignkey 
    como en este caso mas arriba idProyecto
    '''
    def setValues(self,nombreFase, descripcion, estado, fechaInicio, fechaFinalizacion, idProyecto):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type nombreFase : string
        @param nombreFase : nombre de la fase
        @type descripcion : string
        @param descripcion : descripcion de la fase
        @type estado : string
        @param estado : estado actual de la fase
        @type fechaInicio : date
        @param fechaInicio : fecha de inicio de la fase
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion de la fase
        @type idProyecto : number
        @param idProyecto : id del proyecto al que la fase pertenece
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
        @type nombreFase : string
        @param nombreFase : nombre de la fase
        @type descripcion : string
        @param descripcion : descripcion de la fase
        @type estado : string
        @param estado : estado actual de la fase
        @type fechaInicio : date
        @param fechaInicio : fecha de inicio de la fase
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion de la fase
        @type idProyecto : number
        @param idProyecto : id del proyecto al que la fase pertenece
        """
        self.nombreFase=nombreFase; 
        self.descripcion=descripcion;
        self.estado=estado;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.idProyecto=idProyecto;
        