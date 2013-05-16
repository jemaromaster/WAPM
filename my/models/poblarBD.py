from usuarioModelo import Usuario
from proyectoModelo import Proyecto
from permisoModelo import Permiso
from rolSistemaModelo import RolSistema
from bdCreator import Session
from tipoPrimarioModelo import TipoPrimario
import md5
import random
from Proyectos.proyectoController import ProyectoControllerClass
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

def cargarProyecto():
     sesion=Session()
     pc=ProyectoControllerClass()
     estate=["activo", "inactivo"]
     for i in range(0,100):
         for j in range(1,10):
              dia=random.randint(1, 28)
              mes=random.randint(1, 12)
              anho=random.randint(1990, 2020)
              u=Proyecto("Proyecto"+str(i)+"_"+str(j), i, str(mes)+"/"+str(dia)+"/"+str(anho), \
                   str(mes)+"/"+str(dia)+"/"+str(anho), \
                   random.randint(1000, 100000),"observacion"+str(random.randint(1990, 2020)), random.randint(1, 12),estate[random.randint(0, 1)])
              
              pc.controlarProyecto(u,i)
     sesion.commit()
     sesion.close()
     
def cargaEstatica():
    """
    Metodo para cargar los valores estaticos que deben estar presentes en ciertas tablas para poder utilizarlas
    en modulos dentro del sistema.
    """  
    sesion=Session()
    #Carga de valores de roles de sistema
    u=None
    rs1=None
    rs2=None
    rs3=None
    cargarValores=sesion.query(RolSistema).count()
    if cargarValores <= 0:
        rs1=RolSistema("Project Leader","El usuario tendra acceso a la creacion y administracion de proyectos")
        rs2=RolSistema("Administrador","El usuario tendra acceso a la creacion y administracion de usuarios")
        rs3=RolSistema("Miembro","El usuario tendra acceso limitado por roles a los proyectos donde fue asignado")
        sesion.add(rs1)
        sesion.add(rs2)
        sesion.add(rs3)
        
    
    cargaValores=sesion.query(Usuario).count()
    if cargarValores <= 0:
        u=Usuario('super',str(md5.new('super').hexdigest()),'super','super','super@super.super','666'
                  ,'0966666','ninguna','true','sl')
        u.roles_sistema.append(rs1)
        u.roles_sistema.append(rs2)
        u.roles_sistema.append(rs3)
        sesion.add(u)
        
    cargaValores=sesion.query(Permiso).count()
    if cargaValores <= 0:
        p=[]
        
        p.append(Permiso('Consultar Fases','01-001','Consulta atributos de fase'))
        #p.append(Permiso('Edicion Fases','01-011','Edita atributos de fase'))
        p.append(Permiso('Finalizar Fases','01-111','Finaliza (cierra) una fase'))
        
        p.append(Permiso('Consultar Linea Base','02-001','Consulta items en la linea base'))
        p.append(Permiso('Edicion LB','02-011','Administra items en la linea base'))
        p.append(Permiso('Finalizar LB','02-111','Finaliza (cierra) una linea Base'))
    
        p.append(Permiso('Consultar Items','03-001','Consulta atributos item'))
        p.append(Permiso('Edicion Iems','03-011','Crea item y edita atributos de item'))
        p.append(Permiso('Finalizar Fases','03-111','Aprueba item'))
    
        p.append(Permiso('Consultar Tipo Item','04-001','Consulta atributos de tipo item'))
        p.append(Permiso('Edicion Tipo Item','04-011','Crea tipo de item y edita atributos de TI'))
        for permiso in p:
            sesion.add(permiso)
    
    cargaValores=sesion.query(TipoPrimario).count()
    if cargaValores <= 0:
        
        t1=TipoPrimario('Texto', 'String')
        t2=TipoPrimario('Numerico', 'Numeric')
        t3=TipoPrimario('Entero', 'int')
        t4=TipoPrimario('Fecha', 'Date')
        
        sesion.add(t1)
        sesion.add(t2)
        sesion.add(t3)
        sesion.add(t4)
        
    sesion.commit()
    sesion.close()