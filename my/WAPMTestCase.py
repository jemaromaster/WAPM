#import flask
import os
import main
import unittest
import tempfile
import json
import random

class WAPMTestCase(unittest.TestCase):
 
    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
        #main.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(main.app.config['DATABASE'])

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

    #===========================================================================
    # def test_agregarUsuario_OK(self):
    #     """Se prueba agregar un Usuario con nuevo nombre de usuario valido"""
    #     #self.login('username1', 'pass2')
    #     self.test_login_OK()
    #     rera=str(random.randint(-999999999999999999,9999999999999999999))
    #     rv=self.agregarU('[ "0", "0" ]',
    #                      rera,
    #                      '4d186321c1a7f0f354b297e8914ab240',
    #                      '65874',
    #                      'john',
    #                      'smith',
    #                      'john@smith.com',
    #                      'brasil 876',
    #                      '124874',
    #                      'ninguna por ahora',
    #                      'true')
    #     assert 'Usuario guardado correctamente' in rv.data
    #===========================================================================
        
    def test_agregarUsuario_FUsername(self):
        """Se prueba agregar un Usuario con nombre de usuario ya existente"""
        self.test_login_OK()
        rv=self.agregarU('[ "0", "0" ]',
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

    #===========================================================================
    # def test_modificarUsuario_OK(self):
    #     """Se prueba modificar un Usuario, asignandole un nombre de usuario nuevo valido"""
    #     self.test_login_OK()
    #     rera=str(random.randint(-999999999999999999,9999999999999999999))
    #     rv=self.modificarU('3',
    #                      rera,
    #                      'hola',
    #                      '65874',
    #                      'john',
    #                      'smith',
    #                      'john@smith.com',
    #                      'brasil 876',
    #                      '124874',
    #                      'ninguna por ahora',
    #                      'activo')
    #     assert 'Usuario guardado correctamente' in rv.data
    #===========================================================================

    def test_modificarUsuario_FUsername(self):
        """Se prueba modificar un Usuario y asignarle un nombre de usuario ya existente"""
        self.test_login_OK()
        rv=self.modificarU('1',
                         'prueba',
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

    #===========================================================================
    # def test_agregarProyecto_OK(self):    
    #     """Se prueba agregar un Proyecto con un nombre de proyecto nuevo(valido, no existente)"""
    #     self.test_login_OK()
    #     rera='ProjectX'+str(random.randint(-9999999999,9999999999))
    #     rv=self.agregarP(rera,
    #                      '3',
    #                      '5',
    #                      'Proyecto de gran envergadura',
    #                      '500000',
    #                      '12/04/1998',
    #                      '15/08/2001',
    #                      'activo')
    #     assert 'Proyecto guardado correctamente' in rv.data
    #===========================================================================

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
#===============================================================================
# EESTOOO NO DEBERIA FUNCIONAR, ME DEJA MODIFICAR Y PONERLE EL MISMO NOMBRE DE PROYECTO YA EXISTENTE
#===============================================================================
    def test_modificarProyecto_OK(self):    
        """Se prueba modificar un Proyecto, cambiar el nombre de proyecto, a uno nuevo(valido, no existente)"""
        self.test_login_OK()
        rera='ProjectX'+str(random.randint(-9999999999,9999999999))
        rv=self.modificarP('2',
                           'TUVIEJA',
                           '1',
                           '5',
                           'Proyecto de gran envergadura',
                           '500000',
                           '12/04/1998',
                           '15/08/2001',
                           'activo')
        print rv.data
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
                         '12/04/98',
                         '15/08/01',
                         'activo')
        assert 'Ya existe Proyecto con ese nombre' in rv.data


'''    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
'''

if __name__ == '__main__':
    unittest.main()