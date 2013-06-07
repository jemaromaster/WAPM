
import flask.views
from flask import make_response
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from models.bdCreator import Session
from models.instanciaAtributos import InstanciaNumerico, InstanciaCadena, InstanciaEntero, InstanciaFecha, InstanciaTipoItem
from models.historialModelo import HistorialItem, HistorialRelacion

sesion=Session()
class EliminarRelacion(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de eliminacion de \
    alguna relacion al servidor. 
    
    """
    
   
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos para eliminar una relacion dentro de la BD. 
        @type  idRelacion: string
        @param idRelacion: id del la relacion en BD
        @type  version_hijo: string
        @param version_hijo: version del hijo a quien pertence la relacion
        """
        #idFase=flask.request.form['id_Fase']
        idRelacion=flask.request.form['idRelacion']
        version_hijo=flask.request.form['version_hijo']
        
        q=sesion.query(Relacion).filter(Relacion.idRelacion==idRelacion).first()
        
        if q is None:
            sesion.close()
            return make_response('t,No existe relacion con ese id')
        
        
        i=sesion.query(Item).filter(Item.idItem==q.hijo_id).first()
        if(i.version==int(version_hijo)-1): #hay que crear una nueva version del item porque es el primero en eliminar de la version
            
            
            histoItem=HistorialItem(i.nombreItem, i.version, i.prioridad, i.costo, i.complejidad, i.fechaInicio, i.fechaFinalizacion, \
                        i.tipoItem_id,i.estado, i.descripcion, \
                        i.fechaCreacion, i.autorVersion_id, i.idItem)
            sesion.add(histoItem);
            
            i.setValues(i.nombreItem, i.prioridad, i.costo, i.complejidad, i.fechaInicio, i.fechaFinalizacion, \
                        i.tipoItem_id,i.estado, i.descripcion, \
                        i.fechaCreacion, i.autorVersion_id, i.idFase)
            i.version=i.version+1;
            sesion.add(i);
            
            r=sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).all()
            
            for rela in r: #se agrega la relaciones actuales al historial
                histoRel=HistorialRelacion(rela.padre_id, rela.hijo_id, rela.versionHijo)
                rela.versionHijo=rela.versionHijo+1;
                sesion.add(histoRel);
                sesion.merge(rela);
            
            insti=sesion.query(InstanciaTipoItem).filter(InstanciaTipoItem.idItem==i.idItem).all()
            for instancia in insti:
                ie=sesion.query(InstanciaEntero).filter(InstanciaEntero.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for ies in ie:
                    laIE=InstanciaEntero(ies.entero)
                    laIE.version=ies.version+1;
                    laIE.instanciaTipoItem_id=ies.instanciaTipoItem_id;
                    sesion.add(laIE)
                
                iDate=sesion.query(InstanciaFecha).filter(InstanciaFecha.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for dateInst in iDate:
                    laF=InstanciaFecha(dateInst.fecha)
                    laF.version=dateInst.version+1;
                    laF.instanciaTipoItem_id=dateInst.instanciaTipoItem_id;
                    sesion.add(laF)
                
                iNum=sesion.query(InstanciaNumerico).filter(InstanciaNumerico.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for numInst in iNum:
                    laN=InstanciaNumerico(numInst.numerico)
                    laN.version=numInst.version+1;
                    laN.instanciaTipoItem_id=numInst.instanciaTipoItem_id;
                    sesion.add(laN)
                
                iCad=sesion.query(InstanciaCadena).filter(InstanciaCadena.instanciaTipoItem_id==instancia.idInstanciaTipoItem).all()
                for cadInst in iCad:
                    caN=InstanciaCadena(cadInst.cadena)
                    caN.version=cadInst.version+1;
                    caN.instanciaTipoItem_id=cadInst.instanciaTipoItem_id;
                    sesion.add(caN)
        #se realiza el control
        
        elif(i.version==int(version_hijo)): #esta en la misma sesion debe agregar nada mas sin crear nuevo item en el historial
                #nada, se agrega nada mas 
                2+2; 
        else: 
                return make_response('t,Nro de version invalido enviado para eliminar')
            
        sesion.query(Relacion).filter(Relacion.idRelacion==idRelacion).delete();
        sesion.commit();
        sesion.close()
        return make_response('f,Items eliminado correctamente')
    
        
            
        
        