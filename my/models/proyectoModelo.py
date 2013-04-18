from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from bdCreator import Base
import flask.views
class Proyecto(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de PROYECTO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: idProyecto, nombreProyecto, FechaInicio, FechaFinalizacion,
    fases, projectLeader, Observacion, Presupuesto
    """
    #Nombre de la tabla
    __tablename__ = 'PROYECTO'
    
    #Columnas
    idProyecto = Column("id_proyecto",Integer, primary_key=True)
    nombreProyecto =  Column("nombre_proyecto",String(20))
    projectLeaderId=Column("project_leader_id",Integer, ForeignKey("USUARIO.id"))
    fechaInicio=Column("fecha_inicio",Date)
    fechaFinalizacion=Column("fecha_finalizacion" ,Date)
    presupuesto=Column("presupuesto",Float)
    observacion=Column("observacion",String(50))
    nroFases=Column("nro_fases", Integer)
    estado=Column("estado",String(15))
    
    def setValues(self,nombreProyecto,projectLeaderId,fechaInicio,fechaFinalizacion,presupuesto, \
                  observacion,nroFases,estado):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombreProyecto,projectLeaderId,fechaInicio,
        fechaFinalizacion,observacion,fases
        """
        self.nombreProyecto=nombreProyecto;
        self.projectLeaderId=projectLeaderId;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.observacion=observacion;
        self.nroFases=nroFases;
        self.presupuesto=presupuesto;
        self.estado=estado
        
    def __init__(self,nombreProyecto,projectLeaderId,fechaInicio,fechaFinalizacion, \
                  presupuesto,observacion,nroFases,estado):
        self.nombreProyecto=nombreProyecto;
        self.projectLeaderId=projectLeaderId;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.observacion=observacion;
        self.nroFases=nroFases;
        self.presupuesto=presupuesto;
        self.estado=estado;
        