from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views

class TipoPrimario(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de TIPODEATRIBUTO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombre, tipoPrimario
    """
    #Nombre de la tabla
    __tablename__ = 'tipo_primario'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    nombre =  Column("nombre",String(20))
    tipoprimario=Column("nombre_tipo_primario",String(10))
    
    def setValues(self,nombre,tipoPrimario):
        """
        Metodo para establecer valores de la clase
        @type nombre : string
        @param nombre : nombre del tipo primario
        @type tipoPrimario : string
        @param tipoPrimario : descripcion del tipo primario 
        """        
        self.nombre=nombre; self.tipoprimario=tipoPrimario
        
    def __init__(self,nombre,tipoprimario):
        """
        Constructor de la clase
        @type nombre : string
        @param nombre : nombre del tipo primario
        @type tipoPrimario : string
        @param tipoPrimario : descripcion del tipo primario 
        """
        self.nombre=nombre; self.tipoprimario=tipoprimario        