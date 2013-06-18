
from models.bdCreator import Session
from models.lineaBaseModelo import LineaBase
from models.itemModelo import Item, Relacion
from models.faseModelo import Fase

sesion=Session()
listaRomper=dict()
def obtenerHijos(listaItems,idSC): 
    if(listaItems is not None):
        for a in listaItems:
            if(a.estado in ['bloqueado']):
                #se obtienen los hijos 
                s=sesion.query(Item).filter(Relacion.padre_id==a.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all();
                obtenerHijos(s,idSC)
                listaRomper[a.idItem]=a;
                #se obtiene su linea base
                lb=sesion.query(LineaBase).join(LineaBase.items).filter(Item.idItem==a.idItem).filter(LineaBase.estado!="inactiva").first()
                #se obtiene todos los items en LB
                #Si es None es porque su LB se paso a inactiva con una SC que contenia a su padre. 
                if(lb != None):
                    
                    listaItemEnLB=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lb.id).all();
                    
                    for u in listaItemEnLB:
                        listaRomper[u.idItem]=u;
                    lb.estado='inactiva'
                    lb.scAfecto=idSC
                    sesion.merge(lb) 
                
                
            elif a.estado in ['aprobado']:
                s=sesion.query(Item).filter(Relacion.padre_id==a.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all();
                obtenerHijos(s,idSC)
                listaRomper[a.idItem]=a;
            
                
def ejecutarSCLB(listaItemsEnSolicitud,idSC):
    
    print("hola") 
    query=sesion.query(Item).filter(Item.idItem.in_(listaItemsEnSolicitud)).all()
    
    for q in query:
        
        #se obtienen todos los hijos
        s=sesion.query(Item).filter(Relacion.padre_id==q.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all()
        obtenerHijos(s,idSC)
        
        #se obtiene su linea base
        lb=sesion.query(LineaBase).join(LineaBase.items).filter(Item.idItem==q.idItem).filter(LineaBase.estado!="inactiva").first()
        #se obtiene todos los items en LB
        if(lb != None):
            
            listaItemEnLB=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lb.id).all();   
            for u in listaItemEnLB:
                listaRomper[u.idItem]=u;
            lb.estado='inactiva'
            lb.scAfecto=idSC
            sesion.merge(lb) 
        
    #se cargo la lista de los items que son hijos y tambien los items que se encuentran en la mism LB
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
        item.estado="sc_activo"
        sesion.merge(item);
    
    sesion.commit()