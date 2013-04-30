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
    

if __name__ == '__main__':
    unittest.main()