from utils import login_required,controlRol
import flask.views
from flask import jsonify,json, g
import flask
from models.bdCreator import Session
from datetime import date

from models.faseModelo import Fase
from models.proyectoModelo import Proyecto


class ListarFasesComboBox(flask.views.MethodView):
    
    def jasonizar(self, fl):
        """
        Modulo que jasoniza la respuesta.
        @type  fl: Fase[]
        @param fl: Resultado de una consulta que trae los datos de las fases a inicluir en el listado
        de fases que se devolvera al cliente.
        """
        
        cad=''
        pre="["
        print('fl  is '+ str(fl))
        if(fl is not None):
            for f in fl:
                
                strFase=str(f.idFase)
                
                if controlRol(strFase,'fase','consulta')==1:
                    if f.estado=="activa":
                        print('f inside loop  is ' + str(f.idFase))
                        cad=cad+ json.dumps({"idFase":f.idFase , "nombreFase":f.tag+" "+f.nombreFase}, separators=(',',':'));
                        cad=cad + ","
            cad=cad[0:len(cad)-1] 
        else:
            cad=cad+ json.dumps({"idFase":0 , "nombreFase":'ninguna'}, separators=(',',':'));
        cad=pre + cad+"]"
            
        return cad 
    
    @login_required
    def get(self):
        """
        Recibe la peticion de listar fases, segun los parametros que incluya la peticion.
        @type idProyecto:string
        @param idProyecto: indica el proyecto sobre el que se filtraran las fases a listar
        """
        sesion=Session() 
        #se obtiene los datos de post del server
        idProyecto=flask.session['idProyecto']
        '''
        cantComite=sesion.query(Proyecto).filter(Proyecto.idProyecto==idProyecto).join(Proyecto.usuariosComite).count()
        if cantComite % 2 ==0 or cantComite == 0:
            idProyecto=0;
        '''
        fasesLista=sesion.query(Fase).order_by("id asc").filter(Fase.idProyecto==idProyecto).all()
       
        
        respuesta=self.jasonizar(fasesLista)
        sesion.close()
        return respuesta
        