from utils import login_required
import flask.views
import flask
from models.bdCreator import Session
from models.proyectoModelo import Proyecto
from models.usuarioModelo import Usuario
from models.rolProyectoModelo import RolProyecto
from models.permisoModelo import Permiso
from models.faseModelo import Fase

        
class SeleccionarProyectoSesion(flask.views.MethodView):
    
    def newRol(self):
        roles=dict()
        
        permisos=dict()
        permisos['consulta']=0
        permisos['finalizar']=0
        roles['fase']=permisos
        
        
        permisos=dict()
        permisos['consulta']=0
        permisos['administrar']=0
        permisos['finalizar']=0
        roles['lb']=permisos
        
        
        permisos=dict()
        permisos['consulta']=0
        permisos['administrar']=0
        permisos['finalizar']=0
        roles['item']=permisos
        
        
        permisos=dict()
        permisos['consulta']=0
        permisos['administrar']=0
        roles['tipo']=permisos
        
        return roles
    
    def setRoles(self,idProyecto,idUsuario):
        
        listadoPermisosProyecto=dict()
        
        sesion=Session()
        listaPermisos=sesion.query(Permiso.codigo,Fase.idFase).order_by('fase.id').filter(Usuario.id==int(idUsuario)).join(Usuario.roles_proyecto)\
                                    .join(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).join(RolProyecto.permisos).all()
        
        print "longitud lista permisos  " + str(len(listaPermisos))
        faseActual=0
        #rol=self.newRol()
        for permiso in listaPermisos:
            
            
              
            if faseActual!=permiso.idFase:
                '''se crea una estructura vacia que agrupa los permisos segun los componentes (fase==1,lb==2,item==3,tipo==4)'''
                rol=self.newRol()
                faseActual=permiso.idFase
            
            componente=permiso.codigo [:2]
            codigoPermiso= permiso.codigo [3:]
            
            if componente=='01':
                componente='fase'
            elif componente == '02':
                componente='lb'
            elif componente =='03':
                componente='item'
            elif componente =='04':
                componente='tipo'
            
            if codigoPermiso [0:1] == '1':
                codigoPermisoFinal='finalizar'
                rol[componente][codigoPermisoFinal]=1
            if codigoPermiso [1:2] == '1':
                codigoPermisoFinal='administrar'
                rol[componente][codigoPermisoFinal]=1
            if codigoPermiso [2:3] == '1':
                codigoPermisoFinal='consulta'
                rol[componente][codigoPermisoFinal]=1
                 
            stringFase=str(permiso.idFase)
            listadoPermisosProyecto[stringFase]=rol
        print "listado de permisos es  este "+ str(listadoPermisosProyecto)
        flask.session['permisos']=listadoPermisosProyecto
        #print "valor de consulta para fase en el rol :  " + str(roles['fase']['consulta'])
        return
    
    
    @login_required
    def get(self): 
        return "nada"
    @login_required
    def post(self):
        
        idProyecto=flask.request.form['idProyecto']
        print "el proyecto es"+ str(idProyecto)
        
        flask.session['idProyecto']=idProyecto
        
        sesion=Session()
        idProyectoSeleccion=flask.session['idProyecto']
        idUsuario=flask.session['idUsuario']
        comiteProject=sesion.query(Usuario.id).filter(Proyecto.idProyecto==idProyectoSeleccion).join(Proyecto.usuariosComite)\
                                          .filter(Usuario.id==idUsuario).first();
        sesion.close()
        if comiteProject is None:
            flask.session['esComite']=0
        else:
            flask.session['esComite']=1
        
        print "valor de comite es:   " + str(flask.session['esComite'])     
        
        self.setRoles(idProyecto,idUsuario)
        
        return str(flask.session['esComite'])
    