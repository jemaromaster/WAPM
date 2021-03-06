from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float, Numeric
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
#from models.tipoItemModelo import TipoItem
from tipoPrimarioModelo import TipoPrimario
from itemModelo import Item
#from models.atributosModelo import Atributos
from models.bdCreator import Session
sesion=Session()
#from atributosModelo import Atributos
'''
    class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", backref="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
    '''

class InstanciaTipoItem(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de instancia_tipo_item
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__ = 'instancia_tipo_item'
    
    idInstanciaTipoItem=Column("id",Integer, primary_key=True)
    
    nombreCampo=Column("nombre:campo",String(20))
    tipoPrimario=Column("tipo_primario", String(15))
    idItem=Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", backref="instanciaTipoItem")
    
    def setValues(self,itemId, nombreCampo, tp):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type idItem : Integer
        @param idItem : id del item
        @type nombreCampo : string
        @param nombreCampo : nombre del campo
        @type tp : string
        @param tp : Tipo primario asociado
        
        """
        self.idItem=itemId;
        self.nombreCampo= nombreCampo;
        self.tipoPrimario=tp;
      
    def __init__(self,itemId, nombreCampo, tp):
        """
        Constructor de la clase 
        @type idItem : Integer
        @param idItem : id del item
        @type nombreCampo : string
        @param nombreCampo : nombre del campo
        @type tp : string
        @param tp : Tipo primario asociado
        
        """
        self.idItem=itemId;
        self.nombreCampo= nombreCampo;
        self.tipoPrimario=tp;
class InstanciaFecha(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de instancia_fecha
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__ = 'instancia_fecha'
    
    idInstanciaFecha=Column("id",Integer, primary_key=True)
    fecha=Column("fecha", Date)
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version", Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instancia_fecha", uselist=False))
            
    def setValues(self,fecha):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type fecha : date
        @param fecha : fecha de la instancia
        """
        self.fecha=fecha;
       
    def __init__(self,fecha):
        """
        Constructor de la clase 
        @type fecha : date
        @param fecha : fecha de la instancia
        """
        self.fecha=fecha;
      
    
class InstanciaCadena(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de instancia_cadena
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__='instancia_cadena'
    
    idInstanciaCadena=Column("id", Integer, primary_key=True)
    cadena=Column("cadena", String(500))
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version", Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaCad", uselist=False))
    def setValues(self,cadena):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type cadena : String
        @param cadena : Cadena de la instancia
        """
        self.cadena=cadena;
       
       
    def __init__(self,cadena):
        """
        Constructor de la clase 
        @type cadena : String
        @param cadena : Cadena de la instancia
        """
        self.cadena=cadena;
       
class InstanciaNumerico(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de instancia_numerico
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__='instancia_numerico'
    
    idInstanciaNumerico=Column("id", Integer, primary_key=True)
    numerico=Column("numero", Numeric)
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version", Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaNum", uselist=False))
    
    def setValues(self,num):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type num : Integer
        @param num : Valor numerico de la instancia
        """
        self.numerico=num;
       
       
    def __init__(self,num):
        """
        Constructor de la clase 
        @type num : Integer
        @param num : Valor numerico de la instancia
        """
        self.numerico=num;
        
class InstanciaEntero(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de instancia_entero
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    """
    __tablename__='instancia_entero'
    
    idInstanciaEntero=Column("id", Integer, primary_key=True)
    entero=Column("entero", Integer(100))
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version", Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaEntero", uselist=False))
    def setValues(self,entero):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type entero : Integer
        @param entero : Valor entero de la instancia
        """
        self.entero=entero;
       
    def __init__(self,entero):
        """
        Constructor de la clase 
        @type entero : Integer
        @param entero : Valor entero de la instancia
        """
        self.entero=entero;
       