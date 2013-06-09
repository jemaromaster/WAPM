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
        rv=self.modificarU('6',
                         rera,
                         'hola',
                         '65874',
                         'johna',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna',
                         'true')
        print rv.data
        assert 'Usuario guardado correctamente' in rv.data

    def test_modificarUsuario_FUsername(self):
        """Se prueba modificar un Usuario y asignarle un nombre de usuario ya existente"""
        self.test_login_OK()
        rera=str(random.randint(-999999999999999999,9999999999999999999))
        rv=self.modificarU('5',
                         'hola',
                         'hola',
                         '65874',
                         'john',
                         'smith',
                         'john@smith.com',
                         'brasil 876',
                         '124874',
                         'ninguna por ahora',
                         'true')
        assert 'Ya existe el usuario' in rv.data

if __name__ == '__main__':
    unittest.main()