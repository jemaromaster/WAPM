from usuarioModelo import Usuario
from proyectoModelo import Proyecto
from rolSistemaModelo import RolSistema
from bdCreator import Session
import md5
def poblar():
    sesion=Session()
    m=md5.new()
    for i in range(0,3):
        print 'el pass es ' + 'pass'+str(1*(i+1))+ 'su string' +str(md5.new('pass'+str(1*(i+1))).hexdigest())
        u=Usuario('username'+str(1*i),str(md5.new('pass'+str(1*(i+1))).hexdigest()),'nombres'+str(1*(i+2)),'apellidos'+str(1*(i+3)),'email'+str(1*(i+4)),'ci'+str(1*(i+5))
                  ,'telefono'+str(1*(i+6)),'obs'+str(1*(i+7)),'true','direccion'+str(1*(i+9)))
        sesion.add(u)
        
        
        
    
    p=Proyecto('miProyecto','1','12/07/15', '12/12/13', '12000','ninguna',5, 'activo')
    sesion.add(u)
    #sesion.add(p)
    sesion.commit()
    sesion.close()

def cargaEstatica():
    """
    Metodo para cargar los valores estaticos que deben estar presentes en ciertas tablas para poder utilizarlas
    en modulos dentro del sistema.
    """  
    sesion=Session()
    #Carga de valores de roles de sistema
    cargarValores=sesion.query(RolSistema).count()
    if cargarValores <= 0:
        rs1=RolSistema("Project Leader","El usuario tendra acceso a la creacion y administracion de proyectos")
        rs2=RolSistema("Administrador","El usuario tendra acceso a la creacion y administracion de usuarios")
        rs3=RolSistema("Miembro","El usuario tendra acceso limitado por roles a los proyectos donde fue asignado")
        sesion.add(rs1)
        sesion.add(rs2)
        sesion.add(rs3)
        sesion.commit()
        
    #Carga de valores de permisos
    #Carga de valores de tipos de atributos
    sesion.close()