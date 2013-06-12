from sqlalchemy import Column, Integer, String
from bdCreator import Base 
class Usuario(Base):
    """
    Esta clase se utiliza para mapear a sus instancias con la tabla de USUARIO
    Hereda de la clase Base. La clase Base debe ser heredada por todas las 
    clases que mapearan a una tabla.
    Atributos de la clase: id, username, passwd, nombres, apellidos, email,
    ci, telefono, observacion,activo,direccion
    """
    
    #Nombre de la tabla
    __tablename__ = 'usuario'
    
    #Columnas
    id = Column("id",Integer, primary_key=True)
    username =  Column("username",String(20))
    passwd=Column("passwd",String(32))
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
        Metodo para establecer valores de la clase
        @type username : string
        @param username : nombre de usuario
        @type passwd : string
        @param passwd : pass del usuario
        @type nombres : string
        @param nombres : nombres del usuario
        @type apellidos : string
        @param apellidos : apellidos del usuario
        @type email : string
        @param email : email del usuario
        @type ci : string
        @param ci : ci del usuario
        @type observacion : string
        @param observacion : observacion
        @type activo : boolean
        @param activo : indica si el usuario se encuentra activo o inactivo 
        @type direccion : string
        @param direccion : direccion del usuario
        """
        self.username=username;self.passwd=passwd;self.nombres=nombres
        self.apellidos=apellidos;self.email=email;self.ci=ci;self.telefono=telefono
        self.observacion=observacion;self.activo=activo;self.direccion=direccion
        
    def __init__(self,username,passwd,nombres,apellidos,email,ci,telefono,observacion,activo,direccion):
        """
        Constructor de la clase
        @type username : string
        @param username : nombre de usuario
        @type passwd : string
        @param passwd : pass del usuario
        @type nombres : string
        @param nombres : nombres del usuario
        @type apellidos : string
        @param apellidos : apellidos del usuario
        @type email : string
        @param email : email del usuario
        @type ci : string
        @param ci : ci del usuario
        @type observacion : string
        @param observacion : observacion
        @type activo : boolean
        @param activo : indica si el usuario se encuentra activo o inactivo 
        @type direccion : string
        @param direccion : direccion del usuario
        """
        self.username=username;self.passwd=passwd;self.nombres=nombres
        self.apellidos=apellidos;self.email=email;self.ci=ci;self.telefono=telefono
        self.observacion=observacion;self.activo=activo;self.direccion=direccion
        