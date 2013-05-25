from sqlalchemy import Table,Column, Integer, String, ForeignKey, Date, Float, Numeric, TIMESTAMP
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

'''class Historial_InstanciaFecha(Base):
    __tablename__ = 'histo_instancia_fecha'
    
    idInstanciaFecha=Column("id",Integer, primary_key=True)
    fecha=Column("fecha", Date)
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version",Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instancia_fecha", uselist=False))
    
    def setValues(self,fecha):
       self.fecha=fecha;
       
    def __init__(self,fecha):
       self.fecha=fecha;
      
    
class Historial_InstanciaCadena(Base):
    __tablename__='histo_instancia_cadena'
    
    idInstanciaCadena=Column("id", Integer, primary_key=True)
    cadena=Column("cadena", String(500))
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version",Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaCad", uselist=False))
    def setValues(self,cadena):
        self.cadena=cadena;
       
       
    def __init__(self,cadena):
        self.cadena=cadena;
       
class HistorialInstanciaNumerico(Base):
    __tablename__='histo_instancia_numerico'
    
    idInstanciaNumerico=Column("id", Integer, primary_key=True)
    numerico=Column("numero", Numeric(100))
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version",Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaNum", uselist=False))
    
    def setValues(self,num):
        self.numerico=num;
       
       
    def __init__(self,num):
         self.numerico=num;
        
class HistorialInstanciaEntero(Base):
    __tablename__='histo_instancia_entero'
    
    idInstanciaEntero=Column("id", Integer, primary_key=True)
    entero=Column("entero", Integer(100))
    instanciaTipoItem_id=Column(Integer, ForeignKey('instancia_tipo_item.id'))
    version=Column("version",Integer)
    #instanciaTipoItem = relationship("InstanciaTipoItem", backref=backref("instanciaEntero", uselist=False))
    def setValues(self,entero):
        self.entero=entero;
       
    def __init__(self,entero):
        self.entero=entero;'''
        
class HistorialRelacion(Base):
    __tablename__='histo_relacion'
    idRelacion=Column("id",Integer, primary_key=True)
    padre_id = Column(Integer, ForeignKey('item.id'))
    hijo_id = Column(Integer, ForeignKey('item.id'))
    versionHijo=Column("version_hijo",Integer)
    
    padres=relationship("Item", primaryjoin="HistorialRelacion.padre_id==Item.idItem")
    hijos=relationship("Item", primaryjoin="HistorialRelacion.hijo_id==Item.idItem")
    
    def setValues (self, padre_id, hijo_id, versionHijo):
        self.padre_id=padre_id;
        self.hijo_id=hijo_id;
        self.versionHijo=versionHijo;
    
    def __init__(self, padre_id, hijo_id, versionHijo):
        self.padre_id=padre_id;
        self.hijo_id=hijo_id;
        self.versionHijo=versionHijo;
        
class HistorialItem(Base):
    #Nombre de la tabla
    __tablename__ = 'histo_item'
    
    #Columnas
    idHistorialItem = Column("id",Integer, primary_key=True)
    nombreItem =  Column("nombre",String(20))
    version=Column("version",Integer)
    prioridad=Column("prioridad",Integer)
    costo=Column("costo",Integer)
    complejidad=Column("complejidad",Integer)
    fechaInicio=Column("fecha_inicio", Date)
    fechaFinalizacion=Column("fecha_finalizacion", Date)
      
    estado=Column("estado", String(12))
    descripcion=Column("descripcion", String(50))
    #archivoExterno
    fechaCreacion= Column("fecha_creacion",TIMESTAMP)

    #MANY TO ONE
    #autorVersion= relationship('Usuario',backref='item')
    autorVersion_id=Column("autor_version_id",Integer, ForeignKey('usuario.id'))
    idItemFK=Column("id_item_fk",Integer, ForeignKey('item.id'))
    
    
    '''para obtener el one to many desde proyecto (un proyecto, muchas fases se utiliza una foreignkey 
    como en este caso mas arriba idProyecto
    '''
    
    def setValues(self, nombreItem, version, prioridad, costo, complejidad,fechaInicio, \
                  fechaFinalizacion, tipoItem_id, estado, descripcion, \
                  fechaCreacion, autorVersion_id,idItemFK):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: id, nombre, descripcion, estado
        """
              
        self.nombreItem=nombreItem;
        self.version=version;
        self.prioridad=prioridad;
        self.tipoItem_id=tipoItem_id;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.estado=estado;
        self.descripcion=descripcion;
        self.fechaCreacion=fechaCreacion;
        self.autorVersion_id=autorVersion_id;
        
        
        self.costo=costo;
        self.complejidad=complejidad;
        
        self.idItemFK=idItemFK
        
    def __init__(self,nombreItem, version, prioridad, costo, complejidad,fechaInicio, \
                  fechaFinalizacion, tipoItem_id, estado, descripcion, \
                  fechaCreacion, autorVersion_id, idItemFK):
        """
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: id, nombre, descripcion, estado
        """
        
        
        self.nombreItem=nombreItem;
        self.version=version;
        self.prioridad=prioridad;
        self.fechaInicio=fechaInicio;
        self.fechaFinalizacion=fechaFinalizacion;
        self.tipoItem_id=tipoItem_id;
        self.estado=estado;
        self.descripcion=descripcion;
        self.fechaCreacion=fechaCreacion;
        self.autorVersion_id=autorVersion_id;
        
        self.idItemFK=idItemFK
        
        
        self.costo=costo;
        self.complejidad=complejidad;
        
       