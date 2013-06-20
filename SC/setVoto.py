import flask.views
from utils import login_required,miembroComite_required
from models.solicitudCambioModelo import SolicitudCambio
from models.usuarioModelo import Usuario
from models.solicitudCambioModelo import Voto
from models.itemModelo import Item
from models.bdCreator import Session
from ejecutarSolCambios import ejecutarSCLB 

class SetVoto(flask.views.MethodView):
    """
    Clase utilizada cuando se hace una peticion de activacion de 
    proyecto al servidor. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo 
    """
    @login_required
    @miembroComite_required
    def post(self):
    
        voto=flask.request.form['voto']
        idSC=flask.request.form['idSC']
        idUsuario=flask.session['idUsuario']
        sesion=Session()
        
        voto=voto.strip()
        idSC=idSC.strip()
        
        
        if voto != 'si' and voto !='no':
            sesion.close() 
            return "t,Voto no valido"
        if idSC=='' or idSC=='0':
            sesion.close()
            return "t,Solicitud no valida"
        SC=sesion.query(SolicitudCambio).filter(SolicitudCambio.id==idSC).first()
        if SC is None:
            sesion.close()
            return "t,Solicitud no valida"
        
        if SC.estado!= "pendiente":
            sesion.close()
            return "t,La Solicitud ya ha sido procesada"
        
        aprobados=sesion.query(Voto).filter(Voto.solicitud==idSC,Voto.voto=='si').count()
        rechazados=sesion.query(Voto).filter(Voto.solicitud==idSC,Voto.voto=='no').count()
        total=sesion.query(Voto).filter(Voto.solicitud==idSC).count()
        
        setVoto=sesion.query(Voto).filter(Voto.solicitud==idSC,Voto.votante==idUsuario).first()
        if setVoto.voto!='p':
            voto=setVoto.voto
            desicion=''
            if voto=='si':
                desicion='Aprobar'
            if voto=='no':
                desicion='Rechazar'
            return "t,Usted ya ha votado por "+desicion+" la solicitud"
        
        setVoto.voto=voto;
        sesion.add(setVoto)
        
        
        
        desicion=''
        if voto=='si':
            aprobados=aprobados+1
            desicion='Aprobar'
        if voto=='no':
            rechazados=rechazados+1
            desicion='Rechazar'
        
        extraMsj=''
        
        print "resultado de la  operacion es:   " + str(aprobados/float(total))
        if aprobados/float(total) > 0.5:
            extraMsj="La solicitud tiene mayoria en APROBAR. Se ha APROBADO la solicitud "
            listaItemQuery=sesion.query(Item.idItem).filter(SolicitudCambio.id==idSC).join(SolicitudCambio.items).all()
            listaItem=[]
            for it in listaItemQuery:
                listaItem.append(it.idItem)
            for it in listaItem:
                print "item en listado a pasar:  "+ str(it)
                    
            ejecutarSCLB(listaItem,idSC)
            SCaprobada=sesion.query(SolicitudCambio).filter(SolicitudCambio.id==idSC).first()
            SCaprobada.estado='aprobada'
            sesion.add(SCaprobada)
        if  rechazados/float(total) > 0.5:
            extraMsj="La solicitud tiene mayoria en RECHAZAR. Se ha RECHAZADO la solicitud "
            SCrechazada=sesion.query(SolicitudCambio).filter(SolicitudCambio.id==idSC).first()
            SCrechazada.estado='rechazada' 
            sesion.add(SCrechazada)
        sesion.commit()
        sesion.close()    
        return "f,Usted ha votado por "+desicion+" la solicitud "+extraMsj 
    
        
            
