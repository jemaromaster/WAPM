from usuarioModelo import Usuario
from bdCreator import Session
sesion=Session()
for i in range(0,3):
    u=Usuario('username'+str(1*i),'pass'+str(1*(i+1)),'nombres'+str(1*(i+2)),'apellidos'+str(1*(i+3)),'email'+str(1*(i+4)),'ci'+str(1*(i+5))
              ,'telefono'+str(1*(i+6)),'obs'+str(1*(i+7)),'true','direccion'+str(1*(i+9)))
    sesion.add(u)
    sesion.commit()
    sesion.commit()
    sesion.close()    
    


                
   