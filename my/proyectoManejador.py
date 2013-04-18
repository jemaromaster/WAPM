from models.proyectoModelo import Proyecto
from models.bdCreator import Session
from flask import make_response


class ProyectoManejador:
    def guardarProyecto(self, proyect, idProyecto):
        sesion=Session()
        p=proyect;
        
        if(idProyecto!=0):
            p=sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).first()
            p.setValues(proyect.nombreProyecto,proyect.projectLeaderId, \
                        proyect.fechaInicio, proyect.fechaFinalizacion,\
                        proyect.presupuesto,\
                        proyect.observacion,proyect.nroFases,proyect.estado)
        
        sesion.add(p)
        sesion.commit()
        sesion.close()
        
        return make_response("f,Proyecto guardado correctamente")
        
