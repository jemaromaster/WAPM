import flask.views
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:pm@localhost:5432/wapm')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
#Se crean todas las tablas que esten dentro del metadata de la Base    
def initDB():
    """
    Metodo para inicializar el motro ORM de sqlAlchemy.El metodo create_all(engine) para crearlas
    crea las tablas si aun no existen, para ello todos los modelos o clases que mapean a las tablas 
    a crearse deberian haber sido importadas.
    """
    from models.proyectoModelo import Proyecto
    from models.usuarioModelo import Usuario
    #from models.proyectoModelo import miembrosProyectoTabla
    Base.metadata.create_all(engine)      