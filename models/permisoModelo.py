from sqlalchemy import Column, Integer, String
from bdCreator import Base 
class Permiso(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de "permiso"
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, nombre, codigo, descripcion
    """
    #Nombre de la tabla
    __tablename__ = 'permiso'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    codigo=Column("codigo",String(6))
    nombre =  Column("nombre",String(20))
    descripcion=Column("descripcion", String(50))
    
    def __init__(self, nombre, codigo, descripcion):
        """
        Constructor de la clase.
        @type nombre : string
        @param nombre : nombre del permiso
        @type codigo : string
        @param codigo : codigo del permiso 
        @type descripcion : string
        @param descripcion : descripcion del permiso
        """ 
        self.codigo=codigo;self.nombre=nombre;self.descripcion=descripcion
        