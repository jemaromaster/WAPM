from sqlalchemy import Column, Integer, String
from bdCreator import Base
import flask.views
class Usuario(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de USUARIO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, username, passwd, nombres, apellidos, email,
    ci, telefono, observacion,activo,direccion
    """
    #Nombre de la tabla
    __tablename__ = 'USUARIO'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    username =  Column("username",String(20))
    passwd=Column("passwd",String(20))
    nombres=Column("nombres",String(30))
    apellidos=Column("apellidos",String(30))
    email=Column("email",String(30))
    ci=Column("ci",String(10))
    telefono=Column("telefono",String(13))
    observacion=Column("observacion",String(50))
    activo=Column("activo", String(10))
    direccion=Column("direccion", String(30))
    
    def setValues(self,username,passwd,nombres,apellidos,email,ci,telefono,observacion,activo,direccion):
        """
        Metodo para establecer valores de atributos de la clase. 
        Parametros: self,username,passwd,nombres,apellidos,email,ci,telefono,observacion,activo,direccion 
        """
        self.username=username;self.passwd=passwd;self.nombres=nombres
        self.apellidos=apellidos;self.email=email;self.ci=ci;self.telefono=telefono
        self.observacion=observacion;self.activo=activo;self.direccion=direccion
        
    def __init__(self,username,passwd,nombres,apellidos,email,ci,telefono,observacion,activo,direccion):
        """
        Constructor de la clase. Al instanciar la clase se da valor a todos los atributos que la 
        componen. 
        Parametros: self,username,passwd,nombres,apellidos,email,ci,telefono,observacion,activo,direccion 
        """
        self.username=username;self.passwd=passwd;self.nombres=nombres
        self.apellidos=apellidos;self.email=email;self.ci=ci;self.telefono=telefono
        self.observacion=observacion;self.activo=activo;self.direccion=direccion
        