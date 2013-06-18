from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,backref, mapper
from bdCreator import Base
import flask.views
from itemModelo import Item

itemLB= Table('item#linea_base', Base.metadata,
    Column('item', Integer, ForeignKey('item.id')),
    Column('lb', Integer, ForeignKey('linea_base.id'))
)

class LineaBase(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de linea_base
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: idLineaBase, descripcion, estado
    """
    #Nombre de la tabla
    __tablename__ = 'linea_base'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    descripcion=Column("descripcion",String(50))
    estado=Column("estado", String(15))
    idFase = Column(Integer, ForeignKey('fase.id'))
    items=relationship('Item',
                                  secondary=itemLB,
                                  backref='lb')
    scAfecto=Column(Integer, ForeignKey('solicitud_cambio.id'))
    
    #item=
    '''para obtener el one to many desde fase (una fase, muchas lbs se utiliza una foreignkey 
    como en este caso mas arriba fase.id
    '''
    def setValues(self,descripcion, estado,idFase):
        """
        Metodo para establecer valores de atributos de la clase. 
        @type descripcion : string
        @param descripcion : descripcion de la linea base
        @type estado : string
        @param estado : estado actual de la fase        
        @type idFase : Integer
        @param idFase : fase a la que esta relacionada la linea base
        """ 
        self.descripcion=descripcion;
        self.estado=estado;
        self.idFase=idFase;
        
    def __init__(self,descripcion, estado):
        """
        Constructor de la clase 
        @type descripcion : string
        @param descripcion : descripcion de la linea base
        @type estado : string
        @param estado : estado actual de la fase        
        """
        self.descripcion=descripcion;
        self.estado=estado;
        
        