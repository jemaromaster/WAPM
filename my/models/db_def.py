from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:pm@localhost:5432/wapm')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String
  
class Usuario(Base):
    
    __tablename__ = 'USUARIO'
    id = Column("id",Integer, primary_key=True)
    name =  Column("nombre",String(50))
    passwd=Column("passwd",String(50))
    
    def __init__(self,id=None,nom=None,passwd=None):
        self.id=id
        self.name=nom
        self.passwd=passwd
    
    def printMyself(self):
        return "Mi Id es ",id,", me llamo ",self.name," y mi pass es...",self.passwd
    
Base.metadata.create_all(engine)