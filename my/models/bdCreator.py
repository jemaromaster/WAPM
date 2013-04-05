from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:linkano@localhost:5433/wapm')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
#Se crean todas las tablas que esten dentro del metadata de la Base    
def initDB():
    from models import Usuario
    Base.metadata.create_all(engine)      