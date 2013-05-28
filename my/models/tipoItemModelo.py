from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from atributosModelo import Atributos
from faseModelo import Fase





class TipoItem(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de tipo_item
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
                                backref='tipoitem')
    
    fase=relationship('Fase', backref='tipoitem')
    fase_id=Column(Integer,ForeignKey('fase.id'))
    
    def setValues(self,nombreTipoItem,descripcion, estado):
        """
        Metodo para establecer valores de la clase
        @type nombreTipoItem : string
        @param nombreTipoItem : nombre del tipo de item
        @type descripcion : string
        @param descripcion : descripcion del tipo de item 
        @type estado : string
        @param estado : estado del tipo de item
        """        
        self.nombreTipoItem=nombreTipoItem;
        self.descripcion=descripcion;
        self.estado=estado;
        
        
    def __init__(self,nombreTipoItem,descripcion, estado):
        """
        Constructor de la clase
        @type nombreTipoItem : string
        @param nombreTipoItem : nombre del tipo de item
        @type descripcion : string
        @param descripcion : descripcion del tipo de item 
        @type estado : string
        @param estado : estado del tipo de item
        """
        self.nombreTipoItem=nombreTipoItem;
        self.descripcion=descripcion;
        self.estado=estado;



'''mapper(Proyecto,'PROYECTO', properties={

})  '''   