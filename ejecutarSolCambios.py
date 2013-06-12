
from models.bdCreator import Session
from models.lineaBaseModelo import LineaBase
from models.itemModelo import Item, Relacion
from models.faseModelo import Fase

sesion=Session()
listaRomper=dict()
def obtenerHijos(listaItems): 
    if(listaItems is not None):
        for a in listaItems:
            if(a.estado in ['bloqueado']):
                #se obtienen los hijos 
                s=sesion.query(Item).filter(Relacion.padre_id==a.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all();
                obtenerHijos(s)
                listaRomper[a.idItem]=a;
                #se obtiene su linea base
                lb=sesion.query(LineaBase).join(LineaBase.items).filter(Item.idItem==a.idItem).first()
                #se obtiene todos los items en LB
                if(lb.estado!='activa'):
                    
                    listaItemEnLB=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lb.id).all();
                    
                    for u in listaItemEnLB:
                        listaRomper[u.idItem]=u;
                    lb.estado='inactiva'
                    sesion.merge(lb) 
                
                
            elif a.estado in ['aprobado']:
                s=sesion.query(Item).filter(Relacion.padre_id==a.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all();
                obtenerHijos(s)
                listaRomper[a.idItem]=a;
def ejecutarSCLB(listaItemsEnSolicitud):
    
    print("hola") 
    query=sesion.query(Item).filter(Item.idItem.in_(listaItemsEnSolicitud)).all()
    
    for q in query:
        
        #se obtienen todos los hijos
        s=sesion.query(Item).filter(Relacion.padre_id==q.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all()
        obtenerHijos(s)
        
    #se cargo la lista de los items que son hijos
    for ids in listaRomper.keys():
        #cons=sesion.query(Item).filter(Item.idItem==listaRomper[ids].idItem).first()
        if listaRomper[ids].estado=='bloqueado':
            item=listaRomper[ids]
            #se obtiene la fase para pasarla a activar si es necsario
            f=sesion.query(Fase).filter(Fase.idFase==item.idFase).first()
            if(f.estado=="finalizada"):
                f.estado="activa";
                sesion.merge(f)
            item.estado='revision'
            sesion.merge(item)
            #se obtiene la lb 
            
        elif listaRomper[ids].estado=='aprobado':
            item=listaRomper[ids]
            item.estado='revision'
            sesion.merge(item)
        
  
    for item in query:
        item.estado="pendiente"
        sesion.merge(item);
    
    sesion.commit()