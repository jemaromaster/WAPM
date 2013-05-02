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
        rv=self.agregarU('[ "0", "0" ]',
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
        


if __name__ == '__main__':
    unittest.main()