from flask import views, make_response
import flask.views


from models.bdCreator import Session

from models.tipoItemModelo import TipoItem
from models.atributosModelo import Atributos
from tipoItemManejador import TipoItemManejador
from models.tipoPrimarioModelo import TipoPrimario



class TipoItemControllerClass(flask.views.MethodView):
    """Clase controladora del tipo de item, su funcion principal es validar los campos completados por el usuario\
    y mandado por el navegador. \Si existe algun error le responde con un mensaje, sino llama a la clase TipoItemManejador.py"""
   
    def controlarTI(self, ti, idIT, atributos, idProyecto, idFase):
        
        ti.nombreTipoItem=ti.nombreTipoItem.strip()
        ti.descripcion=ti.descripcion.strip()
        ti.estado=ti.estado.strip()
        
        """Se controlan primeramente los campos de TIPO DE ITEM """
       
        '''controla el tamano de los strings'''
         
        if not(1<=len(ti.nombreTipoItem)<=20 and 1<=len(ti.descripcion)<=30 \
              and 1<=len(ti.estado)<=10): 
            return make_response('t,Se supera caracteres de los campos ')
            
        
        
        '''consulta si es que existe ya tipo de item en la fase con ese nombre'''
        
        sesion=Session()
        tipit=sesion.query(TipoItem).filter(TipoItem.fase_id==idFase).filter(TipoItem.nombreTipoItem==ti.nombreTipoItem).first()
        if(idIT==0):
            if(tipit is not None):
                sesion.close()
                return make_response('t,Ya existe el tipo de item con ese nombre en esa fase')
        else:
            if( tipit is not None and str(tipit.idTipoItem) != idIT):
                sesion.close()
                return make_response('t,Ya existe el tipo de item con ese nombre en esa fase al intentar modificar')
        
        """Se crean objeto Atributo y agregan a una lista para su posterior control"""
        lista=[]
        sesion=Session()
       
       
        for at in atributos:
            #print('for'+at['nombreAtributo'])
            #tPrimId=sesion.query(TipoPrimario.id).filter(TipoPrimario.nombre==at['tipoPrimario']).first()
            #tPrim=sesion.query(TipoPrimario).filter(TipoPrimario.id==1).first()
            tPrimId=0;
            if(at['tipoPrimario']=='Texto'):
                tPrimId=1
            elif(at['tipoPrimario']=='Numerico'):
                tPrimId=2
            elif(at['tipoPrimario']=='Entero'):
                tPrimId=3
            elif(at['tipoPrimario']=='Fecha'):
                tPrimId=4
            #if(tPrim is None):
            else:
                sesion.close()
                return make_response('t,Tipo primario invalido')
            '''if(tPrimId is None):
                return make_response('t,Tipo primario invalido')'''
            if(int(at['idAtributosRemoto'])==0):
                at=Atributos(None,at['nombreAtributo'], tPrimId, at['longitudCadena'])
            else:
                at=Atributos(int(at['idAtributosRemoto']),at['nombreAtributo'], tPrimId, at['longitudCadena'])
            lista.append(at)
        sesion.close()
      
        
        listaControlada=[]
        
        
        '''se controla cada uno de los atributos de la lista'''
        for atrib in lista:
           #print 'lalalalal el id de T atrib es'+str(atrib.tipoPrimarioId)
            '''controla el tamano de los strings'''
            if not(1<=len(atrib.nombreAtributo)<=20):
                sesion.close()
                return ('t,Se supera caracteres para el nombre de tributo'+atrib.nombreAtributo)
            
            '''si es que es una cadena se controla el campo longitud, si no,se le coloca 0 como longitud'''
            
            #if(atrib.tipoPrimario.nombre=='Texto'): 
            if(atrib.tipoPrimarioId==1): #si esl atributo es String
               try:
                   atrib.longitudCadena=int(atrib.longitudCadena)
               except:
                   sesion.close()
                   return make_response('t,no es valido el numero ' + atrib.longitudCadena + 'en atributo '+ atrib.nombreAtributo)
               
               if not(1<=atrib.longitudCadena<=1000):
                   sesion.close()
                   return make_response('t,Numeros valido para longitud cadena para atributo:' + atrib.nombreAtributo\
                                             + 'debe ser entre 1 y 500')
            else:
                atrib.longitudCadena=int(0); 
                #print 'numerico su longitud cadena es ' + str(atrib.longitudCadena)
            '''se controla que no exista un atributo con ese nombre en el tipo de item'''
            if(idIT!=0): 
                consulta=sesion.query(Atributos).filter(Atributos.tipoItemId==idIT)\
                                    .filter(Atributos.nombreAtributo==atrib.nombreAtributo).first()
                #print 'consulta es'+ str(consulta)
                if(consulta is not None and consulta.idAtributo!=atrib.idAtributo):
                    sesion.close()
                    return ('t,Ya existe atributo con ese nombre'+atrib.nombreAtributo)
           
            listaControlada.append(atrib)
        
       
            
        timan=TipoItemManejador()
        sesion.close()
        return timan.guardarTipoItem(ti, idIT, listaControlada,idProyecto, idFase)
       
