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
        rv=self.modificarP('10',
                           rera,
                           '1',
                           '5',
                           'Proyecto de gran envergadura',
                           '500000',
                           '12/04/1998',
                           '15/08/2015',
                           'desarrollo')
        assert 'Proyecto guardado correctamente' in rv.data
        
#===============================================================================
#     def test_modificarProyecto_FName(self):    
#         """Se prueba modificar un Proyecto, cambiar el nombre de proyecto, a uno  YA existente)"""
#         self.test_login_OK()
#         rv=self.modificarP('2',
#                          'hola',
#                          '3',
#                          '5',
#                          'Proyecto de gran envergadura',
#                          '500000',
#                          '12/04/1998',
#                          '15/08/2001',
#                          'activo')
#         assert 'Ya existe Proyecto con ese nombre' in rv.data
# 
#     def test_modificarProyecto_FechaInv(self):    
#         """Se prueba modificar un Proyecto, poniendole una fecha invalida"""
#         self.test_login_OK()
#         rv=self.modificarP('2',
#                          'lol',
#                          '3',
#                          '5',
#                          'Proyecto de gran envergadura',
#                          '500000',
#                          '51/84/1998',
#                          '15/08/2001',
#                          'activo')
#         print rv.data
#         assert 'Fecha invalida' in rv.data
#  
#     def test_modificarProyecto_FechaIniFin(self):    
#         """Se prueba modificar un Proyecto, poniendole una fecha de finalizacion anterior a la de inicio"""
#         self.test_login_OK()
#         rv=self.modificarP('2',
#                          'lol',
#                          '3',
#                          '5',
#                          'Proyecto de gran envergadura',
#                          '500000',
#                          '15/08/2010',
#                          '15/08/1985',
#                          'activo')
#         assert 'Fecha finalizacion antes que fecha inicio' in rv.data
#===============================================================================

if __name__ == '__main__':
    unittest.main()