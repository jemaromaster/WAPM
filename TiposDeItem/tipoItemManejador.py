from models.tipoItemModelo import TipoItem 
from models.bdCreator import Session
from flask import make_response
from models.atributosModelo import Atributos
#from models.tipoItemModelo  import Atributos
from models.faseModelo import Fase
class TipoItemManejador:
    """Clase encarga de almacenar los tipo de item en la base de datos"""
    def guardarTipoItem(self, t_item, idT_Item, listaAtributos, idProyecto, idFase):
        sesion=Session()
        ti=t_item;
          
        if(idT_Item!=0): #es un tipo de item a modificar
            ti=sesion.query(TipoItem).filter(TipoItem.idTipoItem==idT_Item).first()
            ti.setValues(t_item.nombreTipoItem,t_item.descripcion, t_item.estado)
            
            #se traen todos los atributos de la BD correspondiente a ese item
            atribListaBD=sesion.query(Atributos).filter(Atributos.tipoItemId==idT_Item).all();
            print(atribListaBD)
            ids=[]
            #se agregar a una lista los ID's de esos atributos en BD
            for atribBD in atribListaBD:
                ids.append(atribBD.idAtributo)
                
            print(ids)
            
            #si existe atributo en la lista 
            for atr in listaAtributos:
                atr.tipoItemId=idT_Item;
                if atr.idAtributo in ids: #si el atributo esat en la lista se eliminar, o sino significa que es nuevo
                    ids.remove(atr.idAtributo)
                sesion.merge(atr)
            
            #todo lo que sobra en la lista se elimina
            for idAEliminar in ids:
                sesion.query(Atributos).filter(Atributos.idAtributo==idAEliminar).delete();
                    
        else:#es un tipo de item nuevo
            miFase=sesion.query(Fase).filter(Fase.idFase==idFase).first()
            ti.fase=miFase;
            ti.atributosItem=listaAtributos #como es nuevo se asume que todos sus atributos son nuevos
            #ti.Atributos.append()
        '''se obtiene la fase para relacionar al tipo de item'''
        
        sesion.add(ti)
        #ti=sesion.query(TipoItem).filter(TipoItem.nombreTipoItem==t_item.nombreTipoItem).first()
        sesion.commit()
         
        #sesion.add(listaAtributos[0])
        """for atrib in listaAtributos:
            atrib.tipoItemId=ti.idTipoItem;
            print 'lalalall' +str(atrib.tipoItemId)
            sesion.add(atrib)"""
            #ti.atributosItem.append(atrib);

        #for atrib in listaAtributos:
        #    atrib.tipoitem=t_item
        
        sesion.close()
        
        return make_response("f,Tipo de item guardado correctamente")
        
