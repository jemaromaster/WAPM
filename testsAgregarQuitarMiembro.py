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

    def agregarMiembro(self, idProyecto, idUsuarioAgregar):
      return self.app.post('/agregarMiembrosProyecto/', data=dict(
          idProyecto=idProyecto,
          idUsuarioAgregar=idUsuarioAgregar
      ), follow_redirects=True)
      
    def test_agregarMiembro_OK(self):
        """Se prueba agregar un Usuario a un proyecto determinado (a uno en donde ese usuario todavia no esta)"""
        self.test_login_OK()
        rv=self.agregarMiembro('3', '3')
        assert 'Usuario agregado correctamente al proyecto' in rv.data
        rv=self.quitarMiembro('2', '3')
        assert 'Usuario eliminado correctamente del proyecto' in rv.data

    #===========================================================================
    #     
    # def test_agregarMiembro_Yaesta(self):
    #     """Se prueba agregar un Usuario a un proyecto en el que el, ya se encuentra"""
    #     self.test_login_OK()
    #     rv=self.agregarMiembro('1', '5')
    #     assert 'Usuario ya existe en proyecto' in rv.data
    #===========================================================================

    def quitarMiembro(self, idProyecto, idUsuario):
      return self.app.post('/QuitarMiembrosProyecto', data=dict(
          idProyecto=idProyecto,
          idUsuario=idUsuario
      ), follow_redirects=True)        


if __name__ == '__main__':
    unittest.main()