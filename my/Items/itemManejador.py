from models.faseModelo import Fase
from models.bdCreator import Session
from flask import make_response
from models.itemModelo import Item, Relacion
from models.atributosModelo import Atributos
from models.instanciaAtributos import InstanciaTipoItem,InstanciaCadena,InstanciaFecha, InstanciaNumerico, InstanciaEntero
from models.historialModelo import HistorialItem, HistorialRelacion
from models.tipoItemModelo import TipoItem

#,HistorialInstanciaFecha, HistorialInstanciaEntero,HistorialInstanciaNumerico, HistorialInstanciaCadena

class ItemManejador:
    """
    Clase que es utilizada para guardar los datos de un item una vez que sus datos han sido 
    controlados. 
    """
    def guardarItem(self, item, idI, lista, esReversion):
        """
        Metodo utilizado para guardar los datos del item
        @type  item: Item
        @param item: Item controlado a guardar
        @type  idI: String
        @param idI: Id del item a guardar. Si item es nuevo id es 0
        @type lista: Atributos[]
        @param lista:lista de atributos
        @type esReversion:String
        @param esReversion:Indica si es una reversion 
        """
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
            
            if (esReversion>0):
                r=sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).all()
                
                for rela in r: #se agrega la relaciones actuales al historial
                    histoRel=HistorialRelacion(rela.padre_id, rela.hijo_id, rela.versionHijo)
                    #rela.versionHijo=rela.versionHijo+1;
                    sesion.add(histoRel);
                    #sesion.merge(rela);
                #se borra las relaciones existentes en la tabla Relacion
                sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).delete();
                
                
                q2=sesion.query(HistorialRelacion).filter(HistorialRelacion.hijo_id==i.idItem)\
                                             .filter(HistorialRelacion.versionHijo==esReversion)\
                                             .all()
                for relInsertar in q2:
                    relReversionada=Relacion(relInsertar.padre_id,relInsertar.hijo_id,i.version+1);
                    sesion.add(relReversionada)
                
            else: #es un imte a modificar SOLO SE COPIA LAS RELACIONES ACTUALES AL HISTORIAL
                #SE CAMBIA LA VERSION A VERSION EN LA TABLA RELACION
                r=sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).all()
                
                for rela in r: #se agrega la relaciones actuales al historial
                    histoRel=HistorialRelacion(rela.padre_id, rela.hijo_id, rela.versionHijo)
                    rela.versionHijo=rela.versionHijo+1;
                    sesion.add(histoRel);
                    sesion.merge(rela);
                    
            i.setValues(item.nombreItem, item.prioridad, item.costo, item.complejidad, item.fechaInicio, item.fechaFinalizacion, \
                        i.tipoItem_id,item.estado, item.descripcion, \
                        item.fechaCreacion, item.autorVersion_id, item.idFase)
            i.version=i.version+1;
           
        
        else: #item nuevo
            2+2 #nada se hace se agrega nada mas
            tipoItem=sesion.query(TipoItem).filter(TipoItem.idTipoItem==i.tipoItem_id).first()
            if(tipoItem is not None and tipoItem.estado=='activo'):
                tipoItem.estado='inst'
                sesion.merge(tipoItem)
        
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
                return make_response('t,no pudo insertar el Item2')
        
        sesion.commit()
        sesion.close()
        
        return make_response("f,Item guardado correctamente")
        
