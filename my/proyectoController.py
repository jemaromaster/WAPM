from flask import views, make_response
import flask.views
from sqlalchemy import Date

from models.proyectoModelo import Proyecto
from models.bdCreator import Session

from proyectoManejador import ProyectoManejador
from datetime import date
class ProyectoControllerClass(flask.views.MethodView):
    
    def controlarProyecto(self, proyecto, idProyecto):
        p=proyecto
        
        p.nombreProyecto=p.nombreProyecto.strip()
        p.observacion=p.observacion.strip()
        try:
            p.presupuesto=float(p.presupuesto)
            p.nroFases=int(p.nroFases)
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
       
        if not(isinstance(p.nroFases, int) and p.nroFases>0):
            return make_response('t,numero de Fases invalido ')
        
        
        '''consulta si es que existe ya proyecto con ese nombre si es nuevo proyecto a crear'''
        if(idProyecto==0):
            sesion=Session()
            pry=sesion.query(Proyecto).filter(Proyecto.nombreProyecto==p.nombreProyecto).first()
            if(pry is not None):
                return make_response('t,Ya existe Proyecto con ese nombre')
        
        um=ProyectoManejador()
        
        return um.guardarProyecto(p, idProyecto)
        