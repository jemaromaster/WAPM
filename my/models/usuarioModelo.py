from sqlalchemy import Column, Integer, String
from bdCreator import Base

class Usuario(Base):
    
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
    obs=Column("observacion",String(50))
    ''' 
    Este constructor no hace falta. Supuestamente con 
    el modo declarativo, este constructor es generado
    por default
    '''
    def __init__(self,username,passwd,nombres,apellidos,email,ci,telefono,obs):
        
        self.username=username;self.passwd=passwd;self.nombres=nombres
        self.apellidos=apellidos;self.email=email;self.ci=ci;self.telefono=telefono
        self.obs=obs
        
    
    #Funcion que imprime una cadena con los datos del Usuario
    def printMyself(self):
        return "Mi Id es ",id,", mi username es ",self.username," y mi pass es...",self.passwd