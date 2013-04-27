from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views

class TipoAtributo(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de TIPODEATRIBUTO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombre, tipoPrimario
    """
    #Nombre de la tabla
    __tablename__ = 'tipo_atributo'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    nombre =  Column("nombre",String(20))
    tipoprimario=Column("tipoprimario",String(10))
    
    def setValues(self,nombre,tipoPrimario):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombre,tipoprimario
        """
        self.nombre=nombre; self.tipoprimario=tipoprimario
        
    def __init__(self,nombre,tipoprimario):
        """
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: self,nombre,tipoprimario 
        """
        self.nombre=nombre; self.tipoprimario=tipoprimario        