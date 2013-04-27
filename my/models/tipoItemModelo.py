from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from atributosModelo import Atributos


tipo_item_atributo_tabla=Table('tipo_item#atributo', Base.metadata,
    Column('TIPO_ITEM', Integer, ForeignKey('tipo_item.id')),
    Column('ATRIBUTO', Integer, ForeignKey('atributos.id'))
)


class TipoItem(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de PROYECTO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: idProyecto, nombreProyecto, FechaInicio, FechaFinalizacion,
    fases, projectLeader, Observacion, Presupuesto
    """
    #Nombre de la tabla
    __tablename__ = 'tipo_item'
    
    #Columnas
    idTipoItem = Column("id",Integer, primary_key=True)
    nombreTipoItem = Column("nombre",String(20))
    estado = Column("estado",String(10))
    descripcion = Column("descripcion",String(30))
    atributosItem=relationship('Atributos',
                                secondary=tipo_item_atributo_tabla,
                                backref='tipoitem')
    
    
    def setValues(self,nombreTipoItem,descripcion):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombreTipoItem, faseId
        """
        self.nombreTipoItem=nombreTipoItem;
        self.descripcion=descripcion;
        
        
    def __init__(self,nombreTipoItem,descripcion):
        self.nombreTipoItem=nombreTipoItem;
        self.descripcion=descripcion;



'''mapper(Proyecto,'PROYECTO', properties={

})  '''   