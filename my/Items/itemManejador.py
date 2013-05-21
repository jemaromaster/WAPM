from models.faseModelo import Fase
from models.bdCreator import Session
from flask import make_response
from models.itemModelo import Item
from models.atributosModelo import Atributos
from models.instanciaAtributos import InstanciaTipoItem,InstanciaCadena,InstanciaFecha, InstanciaNumerico, InstanciaEntero
from models.historialModelo import HistorialItem
#,HistorialInstanciaFecha, HistorialInstanciaEntero,HistorialInstanciaNumerico, HistorialInstanciaCadena

class ItemManejador:
    def guardarItem(self, item, idI, lista):
        sesion=Session()
        i=item;
        i.version=1;
        if(idI!=0): #si es que es un item a modificar
            i=sesion.query(Item).filter(Item.idItem==idI).first()
            
            #se crea un nuevo item para el historial 
            histoItem=HistorialItem(i.nombreItem, i.version, i.prioridad, i.costo, i.complejidad, i.fechaInicio, i.fechaFinalizacion, \
                        i.tipoItem_id,i.estado, i.descripcion, \
                        i.fechaCreacion, i.autorVersion_id, i.idItem)
            sesion.add(histoItem);
            
            i.setValues(item.nombreItem, item.prioridad, item.costo, item.complejidad, item.fechaInicio, item.fechaFinalizacion, \
                        i.tipoItem_id,item.estado, item.descripcion, \
                        item.fechaCreacion, item.autorVersion_id, item.idFase)
            i.version=i.version+1;
           
        
        else: #item nuevo
            2+2 #nada se hace se agrega nada mas
                    
        
        sesion.add(i);
        si=None
        
        if(idI==0):
            si=sesion.query(Item).filter(Item.nombreItem==item.nombreItem).first();
            if (si is not None):
                for at in lista:
                            iti=InstanciaTipoItem(si.idItem, at["nombreAtributo"], at["tipoPrimario"])
                            sesion.add(iti)
                                
                            #sesion.commit()
                                
                            c=sesion.query(InstanciaTipoItem).filter(InstanciaTipoItem.idItem==si.idItem)\
                                        .filter(InstanciaTipoItem.nombreCampo==at["nombreAtributo"]).first()
                            idc=c.idInstanciaTipoItem;
                            if at["tipoPrimario"]=="Texto":
                               
                                inst_cad=InstanciaCadena(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                                
                            elif at["tipoPrimario"]=="Numerico":
                                
                                inst_cad=InstanciaNumerico(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            elif at["tipoPrimario"]=="Entero":
                               
                                inst_cad=InstanciaEntero(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            elif at["tipoPrimario"]=="Fecha":
                                
                                inst_cad=InstanciaFecha(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            
            else:
                sesion.close()
                return make_response('t,no se puDOinsertar el Item')
        else: #item a modificar
            #se obtiene el item a modificar
            si=sesion.query(Item).filter(Item.idItem==idI).first()
            
            if (si is not None):
                for at in lista:
                            c=sesion.query(InstanciaTipoItem).filter(InstanciaTipoItem.idItem==si.idItem)\
                                        .filter(InstanciaTipoItem.nombreCampo==at["nombreAtributo"]).first()
                            idc=c.idInstanciaTipoItem;
                            if at["tipoPrimario"]=="Texto":
                               
                                inst_cad=InstanciaCadena(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                                
                            elif at["tipoPrimario"]=="Numerico":
                                
                                inst_cad=InstanciaNumerico(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            elif at["tipoPrimario"]=="Entero":
                               
                                inst_cad=InstanciaEntero(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            elif at["tipoPrimario"]=="Fecha":
                                
                                inst_cad=InstanciaFecha(at["valor"])
                                inst_cad.instanciaTipoItem_id=idc;
                                inst_cad.version=si.version;
                                sesion.add(inst_cad)
                                #sesion.commit();
                            
            else:
                sesion.close()
                return make_response('t,no se puedo insertar el Item22')
            
        sesion.commit()
        sesion.close()
        
        return make_response("f,Item guardado correctamente")
        
