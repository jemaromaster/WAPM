from models.tipoItemModelo import Tipo_item 
from models.bdCreator import Session
from flask import make_response

class TipoItemManejador:
    def guardarTipoItem(self, t_item, idT_Item):
        sesion=Session()
        ti=t_item;
        if(idTipoItem!=0):
            ti=sesion.query(Tipo_item).filter(Tipo_item.idTipoItem==idT_Item).first()
            ti.setValues(t_item.nombreTipoItem,t_item.descripcion, t_item.faseId)
        
      
        sesion.add(ti)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Tipo de item guardado correctamente")
        
