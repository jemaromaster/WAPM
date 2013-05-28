from flask import make_response
import flask.views

from models.faseModelo import Fase
from models.bdCreator import Session
from faseManejador import FaseManejador
from datetime import datetime
class FaseControllerClass(flask.views.MethodView):
    """
    Clase que es utilizada para controlar los datos recibidos del cliente,
    para asegurarse de que no se almacenen valores inconsistentes en la bd 
    
    """        
    def controlarFase(self, f, idF):
        """
        Metodo utilizado para controlar los datos recibidos del cliente
        @type  f: Fase
        @param f: Fase cuyos datos seran controlados antes de ser almacenados en la bd
        @type  idF: number
        @param idF: El id de la fase. Si es cero, la fase enviada es nueva, sino, es una
            fase ya existente cuyos atributos quieren ser modificados.
        """
        
        f.nombrefase=f.nombreFase.strip()
        #f.fechaInicio=f.fechaInicio.strip()
        #f.fechaFinalizacion=f.fechaFinalizacion.strip()
        f.descripcion=f.descripcion.strip()
        f.estado=f.estado.strip()
        print 'nombre de fase es' + str(f.nombreFase)
        print 'fecha inicio'+str(f.fechaInicio)
        print str(f.fechaFinalizacion)
        
        #try:
        print 'idproyecto ' + str(f.idProyecto)
        f.idProyecto=int(f.idProyecto)
        #except:
        #    return make_response ('t, idProyecto no se pudo castear')
        
        '''controla el tamano de los strings'''
         
        if not(1<=len(f.nombrefase)<=20 \
              and 1<=len(f.descripcion)<=50 and 1<=len(f.estado)<=12 ): 
            return make_response('t,Se supera caracteres de los campos ')
            
        
        '''controla caracterejectLeades validos en el username'''
        
        if not(1<=len(f.nombreFase)<20 \
              and 0<len(f.descripcion)<50):
            return make_response('t,Se supera caracteres de los campos ')
            
        if not(isinstance(f.idProyecto, int)):
            return make_response('t,projectLeaderId invalido no int ')
        
       
        '''consulta si es que existe ya usuario con ese nombre'''
        
        sesion=Session()
        qr=sesion.query(Fase).filter(Fase.idProyecto==f.idProyecto).filter(Fase.nombreFase==f.nombreFase).first()
        
        #print 'consulta es'+ qr
        
        if(idF==0):
            if(qr is not None):
                sesion.close()
                return make_response('t,Ya existe una fase con el nombre indicado')
        else:
            if( qr is not None and str(qr.idFase) != idF ):
                sesion.close()
                return make_response('t,Ya existe una fase con el nombre indicado')
        
        '''cuando la fase es nueva se le setea su tag'''
        if(idF==0):
            nroFasesActuales=sesion.query(Fase).filter(Fase.idProyecto==f.idProyecto).count();
            sum=nroFasesActuales+1
            f.tag="F"+str(sum);
        
        #se valida la fecha 
        print 'fecha' + str(f.fechaInicio[6:10])
        try:
            
            fi=datetime(int(f.fechaInicio[6:10]),\
                             int(f.fechaInicio[3:5]),\
                             int(f.fechaInicio[0:2]))
            ff=datetime(int(f.fechaFinalizacion[6:10]),\
                             int(f.fechaFinalizacion[3:5]),\
                             int(f.fechaFinalizacion[0:2]))
            '''
            fi=datetime(int(f.fechaInicio[6:10]),\
                             int(f.fechaInicio[0:2]),\
                             int(f.fechaInicio[3:5]))
            ff=datetime(int(f.fechaFinalizacion[6:10]),\
                             int(f.fechaFinalizacion[0:2]),\
                             int(f.fechaFinalizacion[3:5]))
            '''
        except:
            sesion.close()
            return make_response('t,Fecha invalida') 
        
        #se controla que fecha inicio sea menor que fecha finalizacion
        if not(fi<=ff):
            sesion.close()
            return make_response('t,Fecha finalizacion antes que fecha inicio')
        fm=FaseManejador()
        sesion.close()
        return fm.guardarFase(f, idF)
        