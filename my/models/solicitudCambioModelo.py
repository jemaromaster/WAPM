from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views

from usuarioModelo import Usuario
from itemModelo import Item
from proyectoModelo import Proyecto

from proyectoModelo import comiteProyectoTabla
from proyectoModelo import miembrosProyectoTabla
'''
votoSolicitud= Table('voto_solicitud', Base.metadata,
    Column('solicitud', Integer, ForeignKey('solicitud_cambio.id')),
    Column('votante', Integer, ForeignKey('usuario.id')),
    Column("voto",String(2))
)
'''
itemSolicitud= Table('item_solicitud', Base.metadata,
    Column('item', Integer, ForeignKey('item.id')),
    Column('solicitud', Integer, ForeignKey('solicitud_cambio.id'))
)
class Voto(Base):
    __tablename__ = 'voto_solicitud'
    
    idVoto = Column("id",Integer, primary_key=True)
    solicitud=Column(Integer, ForeignKey('solicitud_cambio.id'))
    votante=Column(Integer, ForeignKey('usuario.id'))
    voto=Column("voto",String(2))
    
    
    
class SolicitudCambio(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de Solicitud de Cambio
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: idProyecto, nombreProyecto, FechaInicio, FechaFinalizacion,
    fases, projectLeader, Observacion, Presupuesto
    """
    #Nombre de la tabla
    __tablename__ = 'solicitud_cambio'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    descripcion =  Column("descripcion",String(50))
    estado=Column("estado",String(15))
    idSolicitante=Column("id_solicitante",Integer, ForeignKey("usuario.id"))
    idProyecto=Column("id_proyecto",Integer, ForeignKey("proyecto.id_proyecto"))
    
    items=relationship('Item',
                                  secondary=itemSolicitud,
                                  backref='solicitud')
    votos=relationship('Voto')

        
    def __init__(self,descripcion,estado):
        self.descripcion=descripcion;
        self.estado=estado;