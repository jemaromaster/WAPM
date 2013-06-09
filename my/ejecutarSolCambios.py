
from models.bdCreator import Session
from models.lineaBaseModelo import LineaBase
from models.itemModelo import Item, Relacion
from models.faseModelo import Fase

sesion=Session()
def ejecutarSCLB(listaItemsEnSolicitud):
    
    print("hola") 
    query=sesion.query(Item).filter(Item.idItem.in_(listaItemsEnSolicitud)).all()
    
    for q in query:
        
        #se obtienen todos los hijos
        s=sesion.query(Item).filter(Relacion.padre_id==q.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all()
        romperTodo(s)
        
        f=sesion.query(Fase).filter(Fase.idFase==q.idFase).first()
        if(f.estado=="finalizada"):
            f.estado="activa";
            sesion.merge(f)
        if(q.estado=="bloqueado"):
            lb=sesion.query(LineaBase).join(LineaBase.items).filter(Item.idItem==q.idItem).first();
                #itemsLista=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lb.id).filter(Item.idItem!=q.idItem).all()
                
            lb.items.remove(q)
            sesion.merge(lb)
       
            c=sesion.query(LineaBase.items).filter(LineaBase.id==lb.id).count()
            print "longitud de la lb es de:    "+str(c)
            
            if (c==0): #si es que es el ultimo elemento de la LB
                sesion.delete(lb);
        #lb.items.remove(Item)
        #sesion.query(LineaBase).filter(LineaBase.id==lb.id).delete()
        #lb=sesion.query(LineaBase).filter(LineaBase==i.lb).all()
    
    for item in query:
        item.estado="pendiente"
        sesion.merge(item);
    
    sesion.commit()
def romperTodo(listaItems):
    if listaItems is not None:
        for a in listaItems:
            s=sesion.query(Item).filter(Relacion.padre_id==a.idItem).join(Relacion, Relacion.hijo_id==Item.idItem).all();
            romperTodo(s)
            #s=sesion.query(Item).join(Relacion, Relacion.padre_id==Item.idItem).filter(Relacion.padre_id==a.idItem).all();
            if(a.estado=="bloqueado"):
                f=sesion.query(Fase).filter(Fase.idFase==a.idFase).first()
                if(f.estado=="finalizada"):
                    f.estado="activa";
                    sesion.merge(f)
                lb=sesion.query(LineaBase).join(LineaBase.items).filter(Item.idItem==a.idItem).first();
                #itemsLista=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lb.id).filter(Item.idItem!=q.idItem).all()
                
                lb.items.remove(a)
                sesion.merge(lb)
                
                c=sesion.query(LineaBase.items).filter(LineaBase.id==lb.id).count()
                print "longitud de la lb en romper todo es de:    "+str(c)
                if (c==0): #si es que es el ultimo elemento de la LB
                    sesion.delete(lb);
                
                a.estado="revision";
                sesion.merge(a);
                
            elif(a.estado=="aprobado"):
                a.estado="revision";
                sesion.add(a);
            else: 
                return;
            
            