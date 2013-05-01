from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
#from models.tipoItemModelo import TipoItem
from tipoPrimarioModelo import TipoPrimario


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
    longitudCadena=Column("longitud_cadena",Integer)
    
    tipoPrimarioId=Column("id_tipo_primario",Integer, ForeignKey("tipo_primario.id"))
    tipoPrimario=relationship("TipoPrimario", backref='atributosPrimarios')
    #tipoItemId=Column("id_tipo_item",Integer, ForeignKey("TipoItem.idTipoItem"))
#    usuariosMiembros=relationship('Usuario',
#                                  secondary=miembrosProyectoTabla,
#                                  backref='proyectos')
    
    tipoItemId = Column("tipo_item_id",Integer, ForeignKey('tipo_item.id'))
    
    def setValues(self,idAtributo,mbreAtributo,tipoPrimarioId, longitudCadena):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,nombreTipoItem, faseId
        """
        self.idAtributo=idAtributo;
        self.nombreAtributo=nombreAtributo;
        self.tipoPrimarioId=tipoPrimarioId;
        self.longitudCadena=longitudCadena;
        
        
    def __init__(self,idAtributo,nombreAtributo,tipoPrimarioId, longitudCadena):
        self.idAtributo=idAtributo;
        self.nombreAtributo=nombreAtributo;
        self.tipoPrimarioId=tipoPrimarioId;
        self.longitudCadena=longitudCadena;



  