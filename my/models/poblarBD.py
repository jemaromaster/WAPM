from usuarioModelo import Usuario
from proyectoModelo import Proyecto
from proyectoModelo import Proyecto
from bdCreator import Session
import md5
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
    