from usuarioModelo import Usuario
from proyectoModelo import Proyecto
from faseModelo import Fase
from permisoModelo import Permiso
from rolSistemaModelo import RolSistema
from bdCreator import Session
from tipoPrimarioModelo import TipoPrimario
import md5
import random
from Proyectos.proyectoController import ProyectoControllerClass
from models.atributosModelo import Atributos 
from models.tipoItemModelo import TipoItem

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
    

def cargarUsuarios(cant_usuario):
    sesion=Session()
    
    for u in range(0,cant_usuario):
         nombreUser="user_"+str(u);
         password=str(md5.new('super').hexdigest());
         nomb="nombre_"+str(u);
         ape="ape_"+str(u);
         correo=nomb+'@wapm.com'
         ci=random.randint(6000, 100000)
         tel=random.randint(6000, 100000)
         
         user=Usuario(nombreUser,password,nomb,ape,correo,ci
                  ,tel,'ninguna','true','Brasil'+str(u))
         
         sesion.add(user)
    sesion.commit()
    sesion.close()
def cargarProyecto():
     sesion=Session()
     
     #sesion.query(Proyecto).filter(Proyecto.nombreProyecto.like('Proyecto')).all()
     sesion.query(Fase).filter(Fase.nombreFase.like("nombreFase_")).all()
     estate=["activo", "inactivo"]
     for i in range(0,10):
         for j in range(1,10):
              dia1=random.randint(1, 28)
              mes1=random.randint(1, 12)
              anho1=random.randint(1990, 1999)
              
              dia2=random.randint(1, 28)
              mes2=random.randint(1, 12)
              anho2=random.randint(2000, 2020)
              
              
              nombreP="Proyecto"+str(i)+"_"+str(j);
              plId=1
              fechaIni=str(mes2)+"/"+str(dia2)+"/"+str(anho2);
              fechaFin=str(mes1)+"/"+str(dia1)+"/"+str(anho1);
              pres=random.randint(1000, 100000)
              obs="observacion"+str(random.randint(1990, 2020));
              est=estate[random.randint(0, 1)]
              
              u=Proyecto(nombreP,plId,fechaIni,fechaFin, pres,obs,est)
              
              sesion.add(u)
    
     cons=sesion.query(Proyecto).filter(Proyecto.nombreProyecto=="Proyecto"+str(0)+"_"+str(1)).first()
     
     #carga las fases
     for j in range(cons.idProyecto,cons.idProyecto+10):
         for r in range (1,10):
             dia1=random.randint(1, 28)
             mes1=random.randint(1, 12)
             anho1=random.randint(1990, 1999)
                
             dia2=random.randint(1, 28)
             mes2=random.randint(1, 12)
             anho2=random.randint(2000, 2020)
             f=Fase("nombreFase_"+str(j)+"_"+str(r), "descripcion de fase " + str(r), "activo", str(mes1)+"/"+str(dia1)+"/"+str(anho1),\
                  str(mes2)+"/"+str(dia2)+"/"+str(anho2), str(j))
             sesion.add(f);
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
        p.append(Permiso('Finalizar Fases','01-101','Finaliza (cierra) una fase'))
        
        p.append(Permiso('Consultar Linea Base','02-001','Consulta items en la linea base'))
        p.append(Permiso('Edicion LB','02-011','Administra items en la linea base'))
        p.append(Permiso('Finalizar LB','02-101','Finaliza (cierra) una linea Base'))
    
        p.append(Permiso('Consultar Items','03-001','Consulta atributos item'))
        p.append(Permiso('Edicion Iems','03-011','Crea item y edita atributos de item'))
        p.append(Permiso('Aprueba Items','03-101','Aprueba item'))
    
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

def cargarDatosParametricos():
    '''carga de datos script'''
    sesion = Session()
    # usuarios
    nombreUser = "jperez";
    password = str(md5.new('jperez').hexdigest());
    nomb = "juan"
    ape = "perez"
    correo = nombreUser + '@wapm.com'
    ci = random.randint(6000, 100000)
    tel = random.randint(6000, 100000)
    
    user = Usuario(nombreUser, password, nomb, ape, correo, ci
             , tel, 'ninguna', 'true', 'Brasil' + str(u))
    sesion.add(user)
    
    nombreUser = "cgonzalez";
    password = str(md5.new('cgonzalez').hexdigest());
    nomb = "Carlos"
    ape = "Gonzalez"
    correo = nombreUser + '@wapm.com'
    ci = random.randint(6000, 100000)
    tel = random.randint(6000, 100000)
    
    user = Usuario(nombreUser, password, nomb, ape, correo, ci
             , tel, 'ninguna', 'true', 'Brasil' + str(u))
    
    sesion.add(user)
    
    nombreUser = "mbenitez";
    password = str(md5.new('mbenitez').hexdigest());
    nomb = "Maria"
    ape = "Benitez"
    correo = nombreUser + '@wapm.com'
    ci = random.randint(6000, 100000)
    tel = random.randint(6000, 100000)
    
    user = Usuario(nombreUser, password, nomb, ape, correo, ci
             , tel, 'ninguna', 'true', 'Brasil' + str(u))
    
    sesion.add(user)
    
    # Proyectos
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    nombreP = "Edificio"
    plId = 1
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    pres = random.randint(1000, 100000)
    obs = "observacion" + str(random.randint(1990, 2020));
    est = "desarrollo"
    u = Proyecto(nombreP, plId, fechaIni, fechaFin, pres, obs, est)
    sesion.add(u)
    
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    nombreP = "miProyecto02"
    plId = 1
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    pres = random.randint(1000, 100000)
    obs = "observacion" + str(random.randint(1990, 2020));
    est = "desarrollo"
    u = Proyecto(nombreP, plId, fechaIni, fechaFin, pres, obs, est)
    sesion.add(u)
    
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    nombreP = "miProyecto03"
    plId = 1
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    pres = random.randint(1000, 100000)
    obs = "observacion" + str(random.randint(1990, 2020));
    est = "desarrollo"
    u = Proyecto(nombreP, plId, fechaIni, fechaFin, pres, obs, est)
    sesion.add(u)
    
    # Fases
    p=sesion.query(Proyecto.idProyecto).filter(Proyecto.nombreProyecto=="Edificio").first()
    
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    f=Fase('Fase1_Terreno', 'miDescriocion', 'desarrollo',fechaIni, fechaFin,  p.idProyecto)
    nroFasesActuales=sesion.query(Fase).filter(Fase.idProyecto==f.idProyecto).count();
    sum=nroFasesActuales+1
    f.tag="F"+str(sum);
    sesion.add(f)
    
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    f=Fase('Fase2_Cimiento', 'miDescriocion', 'desarrollo',fechaIni, fechaFin,  p.idProyecto)
    nroFasesActuales=sesion.query(Fase).filter(Fase.idProyecto==f.idProyecto).count();
    sum=nroFasesActuales+1
    f.tag="F"+str(sum);
    sesion.add(f)
    
    dia1 = random.randint(1, 28)
    mes1 = random.randint(1, 12)
    anho1 = random.randint(1990, 1999)
    dia2 = random.randint(1, 28)
    mes2 = random.randint(1, 12)
    anho2 = random.randint(2000, 2020)
    fechaIni = str(mes2) + "/" + str(dia2) + "/" + str(anho2);
    fechaFin = str(mes1) + "/" + str(dia1) + "/" + str(anho1);
    f=Fase('Fase3_Columnas', 'miDescriocion', 'activa',fechaIni, fechaFin,  p.idProyecto)
    nroFasesActuales=sesion.query(Fase).filter(Fase.idProyecto==f.idProyecto).count();
    sum=nroFasesActuales+1
    f.tag="F"+str(sum);
    sesion.add(f)
    
    #se debe activar el proyecto
    
    p.estado="activo"
    sesion.add(p)
    fases=sesion.query(Fase).filter(Fase.idProyecto==p.idProyecto).all()
    for fi in fases:
        fi.estado="activa"
        sesion.merge(fi)
    
    
    #Tipo de items 
    lista=[]
    a1=Atributos(None,'Tamanho', 2, 'N/A')
    a2=Atributos(None,'tipo', 1, 20)
    lista.append(a1)
    lista.append(a2)
    ti=TipoItem('arena','midescripcion', 'activo')
    miFase=sesion.query(Fase).filter(Fase.nombreFase=='Fase1_Terreno').first()
    ti.fase=miFase;
    ti.atributosItem=lista
    sesion.add(ti)
    
    lista=[]
    a1=Atributos(None,'Tamanho', 3, 'N/A')
    a2=Atributos(None,'tipo', 1, 20)
    a3=Atributos(None,'tipo2', 1, 20)
    lista.append(a1)
    lista.append(a2)
    lista.append(a3)
    ti=TipoItem('tipo2','midescripcion', 'activo')
    miFase=sesion.query(Fase).filter(Fase.nombreFase=='Fase1_Terreno').first()
    ti.fase=miFase;
    ti.atributosItem=lista
    sesion.add(ti)
    
    
    sesion.commit()
    sesion.close()
