from sqlalchemy import Column,Table, Integer, String,ForeignKey
from bdCreator import Base
from sqlalchemy.orm import relationship, backref
from permisoModelo import Permiso
from usuarioModelo import Usuario

rolProyecto_permiso = Table('rol_proyecto#permiso', Base.metadata,
    Column('permiso_id', Integer, ForeignKey('permiso.id')),
    Column('rol_proyecto_id', Integer, ForeignKey('rol_proyecto.id'))
)

rolProyecto_usuario = Table('rol_proyecto#usuario', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id')),
    Column('rol_proyecto_id', Integer, ForeignKey('rol_proyecto.id'))
)

class RolProyecto(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de rol_proyecto
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombre,descripcion
    """
    #Nombre de la tabla
    __tablename__ = 'rol_proyecto'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    nombre =  Column("nombre",String(20))
    descripcion=Column("descripcion", String(50))
    idFase = Column(Integer, ForeignKey('fase.id'))
    
    permisos = relationship("Permiso", secondary=rolProyecto_permiso, backref=backref('roles_proyecto'))
    usuarios = relationship("Usuario", secondary=rolProyecto_usuario, backref=backref('roles_proyecto'))
    
    def __init__(self,nombre, descripcion):
        """
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: self,id, nombre, descripcion 
        """
        self.nombre=nombre;self.descripcion=descripcion
        