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


if __name__ == '__main__':
    unittest.main()