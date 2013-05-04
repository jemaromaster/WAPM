#import flask
import os
import mainPyUnit
import unittest
import tempfile
import json
import random

class WAPMTestCase(unittest.TestCase):
 
    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, mainPyUnit.app.config['DATABASE'] = tempfile.mkstemp()
        mainPyUnit.app.config['TESTING'] = True
        self.app = mainPyUnit.app.test_client()
        #mainPyUnit.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(mainPyUnit.app.config['DATABASE'])

    def login(self, username, passwd):
        return self.app.post('/', data=dict(
            username=username,
            passwd=passwd
        ), follow_redirects=True)

    def test_login_OK(self):
        """Make sure login and logout works"""
        rv = self.login('super',
                        '1b3231655cebb7a1f783eddf27d254ca')
        assert 'Bienvenido' in rv.data

    def test_login_FUser(self):
        """Prueba autenticarse con usuario inexistente"""
        rv = self.login('usernoexiste',
                        'super')
        assert 'Usuario no existe' in rv.data
 
    def test_login_FPass(self):        
        """Prueba autenticarse con password incorrecto"""
        rv = self.login('super',
                        'passnoexiste')
        assert 'password es incorrecto' in rv.data

    def agregarU(self, rolSistema, nombreUsuario, password, ci, nombre, apellido, email, direccion, telefono, observacion, activo):
      return self.app.post('/agregarUsuario/', data=dict(
          rolSistema=rolSistema,
          nombreUsuario=nombreUsuario,
          password=password,
          ci=ci,
          nombre=nombre,
          apellido=apellido,
          email=email,
          direccion=direccion,
          telefono=telefono,
          observacion=observacion,
          activo=activo
      ), follow_redirects=True)

    def test_agregarUsuario_OK(self):
        """Se prueba agregar un Usuario con nuevo nombre de usuario valido"""
        #self.login('username1', 'pass2')
        self.test_login_OK()
        rera=str(random.randint(-999999999999999999,9999999999999999999))
        rv=self.agregarU('[ "1", "1" ]',
                         rera,
                         '4d186321c1a7f0f354b297e8914ab240',
                         '65874',
                         'john',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna por ahora',
                         'true')
        assert 'Usuario guardado correctamente' in rv.data
        
    def test_agregarUsuario_FUsername(self):
        """Se prueba agregar un Usuario con nombre de usuario ya existente"""
        self.test_login_OK()
        rv=self.agregarU('["0", "0"]',
                         'super',
                         'hola',
                         '65874',
                         'john',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna por ahora',
                         'activo')
        assert 'Ya existe el usuario' in rv.data
         
    def modificarU(self, idUsuario, nombreUsuario, password, ci, nombre, apellido, email, direccion, telefono, observacion, activo):
      return self.app.post('/usuarioManager/modificarUsuario', data=dict(
          idUsuario=idUsuario,
          nombreUsuario=nombreUsuario,
          password=password,
          ci=ci,
          nombre=nombre,
          apellido=apellido,
          email=email,
          direccion=direccion,
          telefono=telefono,
          observacion=observacion,
          activo=activo
      ), follow_redirects=True)

    def test_modificarUsuario_OK(self):
        """Se prueba modificar un Usuario, asignandole un nombre de usuario nuevo valido"""
        self.test_login_OK()
        rera=str(random.randint(-999999999999999999,9999999999999999999))
        rv=self.modificarU('2',
                         rera,
                         'hola',
                         '65874',
                         'johna',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna',
                         'activo')
        print rv.data
        assert 'Usuario guardado correctamente' in rv.data

    def test_modificarUsuario_FUsername(self):
        """Se prueba modificar un Usuario y asignarle un nombre de usuario ya existente"""
        self.test_login_OK()
        rera=str(random.randint(-999999999999999999,9999999999999999999))
        rv=self.modificarU('1',
                         'hola',
                         'hola',
                         '65874',
                         'john',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna por ahora',
                         'activo')
        assert 'Ya existe el usuario' in rv.data
        
    def agregarP(self, nombreProyecto, idUsuario, nroFases, observacion, presupuesto, fechaInicio, fechaFinal, estado):
      return self.app.post('/agregarProyecto/', data=dict(
          nombreProyecto=nombreProyecto,
          idUsuario=idUsuario,
          nroFases=nroFases,
          observacion=observacion,
          presupuesto=presupuesto,
          fechaInicio=fechaInicio,
          fechaFinal=fechaFinal,
          estado=estado
      ), follow_redirects=True)

    def test_agregarProyecto_OK(self):    
        """Se prueba agregar un Proyecto con un nombre de proyecto nuevo(valido, no existente)"""
        self.test_login_OK()
        rera='ProjectX'+str(random.randint(-9999999999,9999999999))
        rv=self.agregarP(rera,
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '12/04/1998',
                         '15/08/2001',
                         'activo')
        assert 'Proyecto guardado correctamente' in rv.data

    def test_agregarProyecto_FName(self):    
        """Se prueba agregar un Proyecto con un nombre de proyecto nuevo(valido, no existente)"""
        self.test_login_OK()
        rv=self.agregarP('hola',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '12/04/1998',
                         '15/08/2001',
                         'activo')
        assert 'Ya existe Proyecto con ese nombre' in rv.data
  
    def test_agregarProyecto_FechaInv(self):    
        """Se prueba agregar un Proyecto con fecha invalida"""
        self.test_login_OK()
        rera='ProjectX'+str(random.randint(-9999999999,9999999999))
        rv=self.agregarP(rera,
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '72/04/1998',
                         '15/08/2001',
                         'activo')
        assert 'Fecha invalida' in rv.data
        
    def test_agregarProyecto_FechaIniFin(self):    
        """Se prueba agregar un Proyecto con fecha de finalizacion anterior a la de inicio"""
        self.test_login_OK()
        rera='ProjectX'+str(random.randint(-9999999999,9999999999))
        rv=self.agregarP(rera,
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '12/04/2015',
                         '15/08/2001',
                         'activo')
        assert 'Fecha finalizacion antes que fecha inicio' in rv.data

    def modificarP(self, idProyecto, nombreProyecto, idProjectLeader, nroFases, observacion, presupuesto, fechaInicio, fechaFinalizacion, estado):
      return self.app.post('/modificarProyecto', data=dict(
          idProyecto=idProyecto,
          nombreProyecto=nombreProyecto,
          idProjectLeader=idProjectLeader,
          nroFases=nroFases,
          observacion=observacion,
          presupuesto=presupuesto,
          fechaInicio=fechaInicio,
          fechaFinalizacion=fechaFinalizacion,
          estado=estado
      ), follow_redirects=True)

 #==============================================================================
 # EESTOOO NO DEBERIA FUNCIONAR, ME DEJA MODIFICAR Y PONERLE EL MISMO NOMBRE DE PROYECTO YA EXISTENTE
 #==============================================================================
    def test_modificarProyecto_OK(self):    
        """Se prueba modificar un Proyecto, cambiar el nombre de proyecto, a uno nuevo(valido, no existente)"""
        self.test_login_OK()
        rera='ProjectX'+str(random.randint(-9999999999,9999999999))
        rv=self.modificarP('2',
                           rera,
                           '1',
                           '5',
                           'Proyecto de gran envergadura',
                           '500000',
                           '12/04/1998',
                           '15/08/2001',
                           'activo')
        assert 'Proyecto guardado correctamente' in rv.data
        
    def test_modificarProyecto_FName(self):    
        """Se prueba modificar un Proyecto, cambiar el nombre de proyecto, a uno  YA existente)"""
        self.test_login_OK()
        rv=self.modificarP('2',
                         'hola',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '12/04/1998',
                         '15/08/2001',
                         'activo')
        assert 'Ya existe Proyecto con ese nombre' in rv.data

    def test_modificarProyecto_FechaInv(self):    
        """Se prueba modificar un Proyecto, poniendole una fecha invalida"""
        self.test_login_OK()
        rv=self.modificarP('2',
                         'lol',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '51/84/1998',
                         '15/08/2001',
                         'activo')
        print rv.data
        assert 'Fecha invalida' in rv.data
 
    def test_modificarProyecto_FechaIniFin(self):    
        """Se prueba modificar un Proyecto, poniendole una fecha de finalizacion anterior a la de inicio"""
        self.test_login_OK()
        rv=self.modificarP('2',
                         'lol',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '15/08/2010',
                         '15/08/1985',
                         'activo')
        assert 'Fecha finalizacion antes que fecha inicio' in rv.data
        
    def agregarMiembro(self, idProyecto, idUsuarioAgregar):
      return self.app.post('/agregarMiembrosProyecto/', data=dict(
          idProyecto=idProyecto,
          idUsuarioAgregar=idUsuarioAgregar
      ), follow_redirects=True)
      
    def test_agregarMiembro_OK(self):
        """Se prueba agregar un Usuario a un proyecto determinado (a uno en donde ese usuario todavia no esta)"""
        self.test_login_OK()
        rv=self.agregarMiembro('2', '3')
        assert 'Usuario agregado correctamente al proyecto' in rv.data
        rv=self.quitarMiembro('2', '3')
        assert 'Usuario eliminado correctamente del proyecto' in rv.data

        
    def test_agregarMiembro_Yaesta(self):
        """Se prueba agregar un Usuario a un proyecto en el que el, ya se encuentra"""
        self.test_login_OK()
        rv=self.agregarMiembro('1', '5')
        assert 'Usuario ya existe en proyecto' in rv.data

    def quitarMiembro(self, idProyecto, idUsuario):
      return self.app.post('/QuitarMiembrosProyecto', data=dict(
          idProyecto=idProyecto,
          idUsuario=idUsuario
      ), follow_redirects=True)        
    #===========================================================================
    # def test_quitarMiembro_OK(self):
    #     self.test_login_OK()
    #     rv=self.quitarMiembro('2', '3')
    #     print rv.data
    #     assert 'Usuario eliminado correctamente del proyecto' in rv.data
    #===========================================================================

    def agregar_Fase(self, nombreFase, fechaInicio, fechaFinal, descripcion, estado, idProyecto):
      return self.app.post('/agregarFase/', data=dict(
          nombreFase=nombreFase,
          fechaInicio=fechaInicio,
          fechaFinal=fechaFinal,
          descripcion=descripcion,
          estado=estado,
          idProyecto=idProyecto
      ), follow_redirects=True)           
     
    def test_agregarFase_OK(self):
        """Se prueba agregar una fase con un nombre valido(no existente)"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))        
        rv= self.agregar_Fase(rera, '12/04/1998', '20/04/1998', 'ninguna', 'activa', '3')   
        assert 'Fase guardada correctamente' in rv.data
        
    def test_agregarFase_YA(self):
        """Se prueba agregar una fase con un nombre ya existente"""
        self.test_login_OK()
        rv= self.agregar_Fase('primera', '12/04/1998', '20/04/1998', 'ninguna', 'activa', '3')   
        assert 'Ya existe una fase con el nombre indicado' in rv.data

    def test_agregarFase_FechaInv(self):
        """Se prueba agregar una fase con una fecha invalida"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))        
        rv= self.agregar_Fase(rera, '12/04/1998', '31/04/1998', 'ninguna', 'activa', '3')   
        assert 'Fecha invalida' in rv.data

    def test_agregarFase_FechaIniFin(self):
        """Se prueba agregar una fase con una fecha de finalizacion anterior a la de inicio"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))        
        rv= self.agregar_Fase(rera, '12/06/1998', '30/04/1998', 'ninguna', 'activa', '3')   
        assert 'Fecha finalizacion antes que fecha inicio' in rv.data
                        
    def modificar_Fase(self, idFase, nombreFase, fechaInicio, fechaFinal, descripcion, estado, idProyecto):
      return self.app.post('/modificarFase/', data=dict(
          idFase=idFase,
          nombreFase=nombreFase,
          fechaInicio=fechaInicio,
          fechaFinal=fechaFinal,
          descripcion=descripcion,
          estado=estado,
          idProyecto=idProyecto
      ), follow_redirects=True)    
    
    def test_modificarFase_OK(self):
        """Se prueba modificar una fase, poniendole un nombre valido(no existe)"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))
        rv=self.modificar_Fase('2',
                         rera,
                         '20/05/1998',
                         '21/06/2000',
                         'heello flow',
                         'activa',
                         '2')
        assert 'Fase guardada correctamente' in rv.data

    def test_modificarFase_YaEsta(self):
        """Se prueba modificar una fase, poniendole un nombre ya existente"""
        self.test_login_OK()
        rv=self.modificar_Fase('3',
                         'ya_estoy',
                         '20/05/2013',
                         '21/06/2013',
                         'heello flow',
                         'Activo',
                         '6')
        assert 'Ya existe una fase con el nombre indicado' in rv.data
 
    def test_modificarFase_FechaInv(self):
        """Se prueba modificar una fase, poniendole una fecha invalida"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))
        rv=self.modificar_Fase('2',
                         rera,
                         '58/31/1998',
                         '21/06/2000',
                         'heello flow',
                         'activa',
                         '2')
        assert 'Fecha invalida' in rv.data
 
    def test_modificarFase_FechaIniFin(self):
        """Se prueba modificar una fase, poniendole una fecha de finalizacion anterior a la de inicio"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))
        rv=self.modificar_Fase('2',
                         rera,
                         '20/05/2000',
                         '21/06/1998',
                         'heello flow',
                         'activa',
                         '2')
        assert 'Fecha finalizacion antes que fecha inicio' in rv.data
        
    def agregarTipoItem(self, nombreTipoItem, estado, descripcion, atributos, idProyecto, idFase):
      return self.app.post('/agregarTipoItem/', data=dict(
          nombreTipoItem=nombreTipoItem,
          estado=estado,
          descripcion=descripcion,
          atributos=atributos,
          idProyecto=idProyecto,
          idFase=idFase
      ), follow_redirects=True)    
        
    def test_agregarTipoItem_OK(self):
        """Se prueba agregar un Tipo de item con nombre valido(no existente)"""
        self.test_login_OK()
        rera=str(random.randint(-9999999999,9999999999))
        rv=self.agregarTipoItem(rera,
                             'Activo',
                             'juego, web, editor',
                             '[{"idAtributosLocal":"4","idAtributosRemoto":"0","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"3","idAtributosRemoto":"0","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '2',
                             '1')
        assert 'Tipo de item guardado correctamente' in rv.data

    def test_agregarTipoItem_Yaesta(self):
        """Se prueba agregar un Tipo de item con nombre ya existente"""
        self.test_login_OK()
        rv=self.agregarTipoItem('hola',
                             'Activo',
                             ' web, editor',
                             '[{"idAtributosLocal":"4","idAtributosRemoto":"0","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"3","idAtributosRemoto":"0","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '2',
                             '1')
        assert 'Ya existe el tipo de item con ese nombre en esa fase' in rv.data

    def modificarTipoItem(self, idTipoItem, nombreTipoItem, estado, descripcion, atributos, idProyecto, idFase):
      return self.app.post('/modificarTipoItem/', data=dict(
          idTipoItem=idTipoItem,
          nombreTipoItem=nombreTipoItem,
          estado=estado,
          descripcion=descripcion,
          atributos=atributos,
          idProyecto=idProyecto,
          idFase=idFase
      ), follow_redirects=True)    
        
    def modificarTipoItem(self, idTipoItem, nombreTipoItem, estado, descripcion, atributos, idProyecto, idFase):
      return self.app.post('/modificarTipoItem/', data=dict(
          idTipoItem=idTipoItem,
          nombreTipoItem=nombreTipoItem,
          estado=estado,
          descripcion=descripcion,
          atributos=atributos,
          idProyecto=idProyecto,
          idFase=idFase
      ), follow_redirects=True)    
        
    def test_modificarTipoItem_OK(self):
        """Se prueba modificar un Tipo de item a uno con nombre valido(no existente)"""
        self.test_login_OK()
        rera=str(random.randint(-9999,99999))
        rv=self.modificarTipoItem('3',
                                 rera,
                             'activo',
                             'juegow',
                             '[{"idAtributosLocal":"1","idAtributosRemoto":"40","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"2","idAtributosRemoto":"41","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '1',
                             '3')
        assert 'Tipo de item guardado correctamente' in rv.data

    def test_modificarTipoItem_Yaesta(self):
        """Se prueba agregar un Tipo de item con nombre ya existente"""
        self.test_login_OK()
        rv=self.modificarTipoItem('24',
                                  'hola',
                             #'Activo', con este no anda
                             'activo',
                             ' web, editor,23,7',
                             '[{"idAtributosLocal":"1","idAtributosRemoto":"40","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"2","idAtributosRemoto":"41","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '2',
                             '1')
        assert 'Ya existe el tipo de item con ese nombre en esa fase al intentar modificar' in rv.data


if __name__ == '__main__':
    unittest.main()