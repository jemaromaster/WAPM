from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float, Binary 
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
#from models.tipoItemModelo import TipoItem
from tipoPrimarioModelo import TipoPrimario


'''tipoItemTabla= Table('atributos_2', Base.metadata,
    Column('TIPO_ATRIBUTO', Integer, ForeignKey('tipo_atributo.id')),
    Column('TIPO_ITEM', Integer, ForeignKey('tipo_item.id'))
)'''

class Archivos(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de TIPOSDEITEM
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombreAtributo, TipoAtributo, TipoItem
    """
    #Nombre de la tabla
    __tablename__ = 'archivos'
    
    #Columnas
    idArchivo = Column("id",Integer, primary_key=True)
    nombreArchivo = Column("nombre",String(50))
    #path=Column("path",String(100))
    file=Column('file', Binary)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", backref="archivo")
    
    def setValues(self,nombreArchivo,file, item_id):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombreTipoItem, faseId
        """
        self.nombreArchivo=nombreArchivo;
        self.file=file;
        self.item_id=item_id;
        
    def __init__(self,nombreArchivo, file, item_id):
        self.nombreArchivo=nombreArchivo;
        self.file=file;
        self.item_id=item_id;


