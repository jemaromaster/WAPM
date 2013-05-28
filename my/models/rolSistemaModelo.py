from sqlalchemy import Column,Table, Integer, String,ForeignKey
from bdCreator import Base
from sqlalchemy.orm import relationship, backref
from usuarioModelo import Usuario


rolSistema_usuario = Table('rol_sistema#usuario', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id')),
    Column('rol_sistema_id', Integer, ForeignKey('rol_sistema.id'))
)

class RolSistema(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de ROLSISTEMA
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, username, passwd, nombres, apellidos, email,
    ci, telefono, observacion,activo,direccion
    """
    __tablename__ = 'rol_sistema'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    

    usuarios = relationship("Usuario", secondary=rolSistema_usuario, backref=backref('roles_sistema'))

    def __init__(self, nombre,descripcion):
        """
        Constructor de la clase
        @type nombre : string
        @param nombre : nombre del rol de sistema
        @type descripcion : string
        @param descripcion : descripcion del rol de sistema 
        @type estado : string
        @param estado : estado del rol de sistema
        """
        self.nombre=nombre
        self.descripcion=descripcion