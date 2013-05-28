from flask import views, make_response
import flask.views
from sqlalchemy import Date

from models.proyectoModelo import Proyecto
from models.bdCreator import Session

from proyectoManejador import ProyectoManejador
from datetime import datetime
class ProyectoControllerClass(flask.views.MethodView):
    
    def controlarProyecto(self, proyecto, idProyecto):
        p=proyecto
        
        p.nombreProyecto=p.nombreProyecto.strip()
        p.observacion=p.observacion.strip()
        try:
            p.presupuesto=float(p.presupuesto)
            p.projectLeaderId=int(p.projectLeaderId)
        except:
            return make_response('t, presupuesto invalido o nro de fases invalido o \
                                projectLeaderId invalido ')
        
        '''controla el tamano de los strings, si son validos los enteros '''
         
        if not(1<=len(p.nombreProyecto)<20 \
              and 0<=len(p.observacion)<50):
            return make_response('t,Se supera caracteres de los campos ')
            
        if not(isinstance(p.projectLeaderId, int)):
            return make_response('t,projectLeaderId invalido no int ')
        
        
        if not(isinstance(p.presupuesto, float) and p.presupuesto>=float(0.0)):
            return make_response('t,PRESUPUESTO invalido')
        
        
        '''consulta si es que existe ya proyecto con ese nombre si es nuevo proyecto a crear'''
        sesion=Session()
        if(idProyecto==0):
            pry=sesion.query(Proyecto).filter(Proyecto.nombreProyecto==p.nombreProyecto).first()
            if(pry is not None):
                sesion.close()
                return make_response('t,Ya existe Proyecto con ese nombre')
        else:
            pry=sesion.query(Proyecto).filter(Proyecto.nombreProyecto==p.nombreProyecto).first()
            if(pry is not None and int(pry.idProyecto)!=int(idProyecto)):
                sesion.close()
                return make_response('t,Ya existe Proyecto con ese nombre')
        print "fecha de inicio de proyecto"+p.fechaInicio[3:5]+ p.fechaInicio[0:2]
        print p.fechaFinalizacion
        try:
            '''
            fi=datetime(int(p.fechaInicio[6:10]),\
                             int(p.fechaInicio[3:5]),\
                             int(p.fechaInicio[0:2]))
            ff=datetime(int(p.fechaFinalizacion[6:10]),\
                             int(p.fechaFinalizacion[3:5]),\
                             int(p.fechaFinalizacion[0:2]))
            '''
            fi=datetime(int(p.fechaInicio[6:10]),\
                             int(p.fechaInicio[0:2]),\
                             int(p.fechaInicio[3:5]))
            ff=datetime(int(p.fechaFinalizacion[6:10]),\
                             int(p.fechaFinalizacion[0:2]),\
                             int(p.fechaFinalizacion[3:5]))
            
        except:
            sesion.close()
            return make_response('t,Fecha invalida') 
        
        if not(fi<=ff):
            sesion.close()
            return make_response('t,Fecha finalizacion antes que fecha inicio')
        um=ProyectoManejador()
        sesion.close()
        return um.guardarProyecto(p, idProyecto)
        