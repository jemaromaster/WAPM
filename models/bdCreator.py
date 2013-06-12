from sqlalchemy import create_engine
from config import DEV

#engine = create_engine('postgresql://postgres:linkano@localhost:5433/wapm')
#engine = create_engine('postgresql://postgres:pm@localhost:5432/WAPM_PROD')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
if DEV == True:
    #engine = create_engine('postgresql://postgres:linkano@localhost:5433/wapm')
    engine = create_engine('postgresql://postgres:pm@localhost:5432/wapm')
    print "ambiente de desarrollo"
else:
    #engine = create_engine('postgresql://postgres:linkano@localhost:5433/wapm_prod2')
    engine = create_engine('postgresql://postgres:pm@localhost:5432/cargada2')
    print "ambiente de produccion"
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
    from permisoModelo import Permiso
    from rolProyectoModelo import RolProyecto
    from tipoItemModelo import TipoItem
    from tipoPrimarioModelo import TipoPrimario
    from itemModelo import Item, Relacion
    from instanciaAtributos import InstanciaTipoItem,InstanciaFecha, InstanciaCadena, InstanciaNumerico, InstanciaEntero
    from atributosModelo import Atributos
    from historialModelo import HistorialItem, HistorialRelacion
    from lineaBaseModelo import LineaBase
    from solicitudCambioModelo import SolicitudCambio
    from solicitudCambioModelo import Voto 
    from archivosModelo import Archivos   
    Base.metadata.create_all(engine)