from sqlalchemy import create_engine
#engine = create_engine('postgresql://postgres:linkano@localhost:5433/wapm')
engine = create_engine('postgresql://postgres:postgres@localhost:5432/wapm')

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
    from usuarioModelo import Usuario
    from proyectoModelo import Proyecto
    from proyectoModelo import miembrosProyectoTabla
    from rolSistemaModelo import RolSistema
    
    from faseModelo import Fase
    from tipoItemModelo import TipoItem
    from tipoPrimarioModelo import TipoPrimario
    from atributosModelo import Atributos
    
    

    Base.metadata.create_all(engine)