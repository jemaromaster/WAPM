from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from usuarioModelo import Usuario


miembrosProyectoTabla= Table('miembros_proyecto', Base.metadata,
    Column('proyecto', Integer, ForeignKey('proyecto.id_proyecto')),
    Column('usuario', Integer, ForeignKey('usuario.id'))
)
comiteProyectoTabla= Table('comite_proyecto', Base.metadata,
    Column('proyecto', Integer, ForeignKey('proyecto.id_proyecto')),
    Column('usuario', Integer, ForeignKey('usuario.id'))
)

class Proyecto(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de PROYECTO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: idProyecto, nombreProyecto, FechaInicio, FechaFinalizacion,
    fases, projectLeader, Observacion, Presupuesto
    """
    #Nombre de la tabla
    __tablename__ = 'proyecto'
    
    #Columnas
    idProyecto = Column("id_proyecto",Integer, primary_key=True)
    nombreProyecto =  Column("nombre_proyecto",String(20))
    projectLeaderId=Column("project_leader_id",Integer, ForeignKey("usuario.id"))
    fechaInicio=Column("fecha_inicio",Date)
    fechaFinalizacion=Column("fecha_finalizacion" ,Date)
    presupuesto=Column("presupuesto",Float)
    observacion=Column("observacion",String(50))
    estado=Column("estado",String(15))
    
    usuariosMiembros=relationship('Usuario',
                                  secondary=miembrosProyectoTabla,
                                  backref='proyectos')
    usuariosComite=relationship('Usuario',
                                  secondary=comiteProyectoTabla,
                                  backref='proyectosComite')
    
    def setValues(self,nombreProyecto,projectLeaderId,fechaInicio,fechaFinalizacion,presupuesto, \
                  observacion,estado):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type nombreProyecto : string
        @param nombreProyecto : nombre del proyecto
        @type projectLeaderId : Integer
        @param projectLeaderId : id del project leader 
        @type fechaInicio : date
        @param fechaInicio : fecha de inicio del proyecto
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion del proyecto
        @type presupuesto : Integer
        @param presupuesto : presupuesto aproximado para el proyecto
        @type observacion : string
        @param observacion : observacion dentro del proyecto
        @type estado : string
        @param estado : estado del proyecto
        """
        self.nombreProyecto=nombreProyecto;
        self.projectLeaderId=projectLeaderId;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.observacion=observacion;
        self.presupuesto=presupuesto;
        self.estado=estado
        
    def __init__(self,nombreProyecto,projectLeaderId,fechaInicio,fechaFinalizacion, \
                  presupuesto,observacion,estado):
        """
        Constructor de la clase 
        @type nombreProyecto : string
        @param nombreProyecto : nombre del proyecto
        @type projectLeaderId : Integer
        @param projectLeaderId : id del project leader 
        @type fechaInicio : date
        @param fechaInicio : fecha de inicio del proyecto
        @type fechaFinalizacion : date
        @param fechaFinalizacion : fecha de finalizacion del proyecto
        @type presupuesto : Integer
        @param presupuesto : presupuesto aproximado para el proyecto
        @type observacion : string
        @param observacion : observacion dentro del proyecto
        @type estado : string
        @param estado : estado del proyecto
        """
        self.nombreProyecto=nombreProyecto;
        self.projectLeaderId=projectLeaderId;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.observacion=observacion;
        self.presupuesto=presupuesto;
        self.estado=estado;