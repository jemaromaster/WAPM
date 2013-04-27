from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
#from models.tipoItemModelo import TipoItem
from tipoAtributoModelo import TipoAtributo


'''tipoItemTabla= Table('atributos_2', Base.metadata,
    Column('TIPO_ATRIBUTO', Integer, ForeignKey('tipo_atributo.id')),
    Column('TIPO_ITEM', Integer, ForeignKey('tipo_item.id'))
)'''

class Atributos(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de TIPOSDEITEM
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombreAtributo, TipoAtributo, TipoItem
    """
    #Nombre de la tabla
    __tablename__ = 'atributos'
    
    #Columnas
    idAtributo = Column("id",Integer, primary_key=True)
    nombreAtributo = Column("nombre",String(20))
    tipoAtributoId=Column("id_tipo_atributo",Integer, ForeignKey("tipo_atributo.id"))
    tipoAtributo=relationship("TipoAtributo", backref='atributos')
    #tipoItemId=Column("id_tipo_item",Integer, ForeignKey("TipoItem.idTipoItem"))
#    usuariosMiembros=relationship('Usuario',
#                                  secondary=miembrosProyectoTabla,
#                                  backref='proyectos')
    
    def setValues(self,nombreAtributo,tipoAtributoId):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombreTipoItem, faseId
        """
        self.nombreAtributo=nombreAtributo;
        self.tipoAtributoId=tipoAtributoId;
       
        
        
    def __init__(self,nombreAtributo,tipoAtributoId):
        self.nombreAtributo=nombreAtributo;
        self.tipoAtributoId=tipoAtributoId;



  