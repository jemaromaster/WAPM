#import flask
import os
import mainPyUnit
import unittest
import tempfile
import json
import random

class TestsLogin(unittest.TestCase):
 
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
        
if __name__ == '__main__':
    unittest.main()