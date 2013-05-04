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
        rera=str(random.randint(-9999999999,9999999999))
        rv=self.modificarTipoItem('24',
                                 rera,
                             'activo',
                             'juego, web, editor,23,17',
                             '[{"idAtributosLocal":"1","idAtributosRemoto":"40","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"2","idAtributosRemoto":"41","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '2',
                             '1')
        assert 'Tipo de item guardado correctamente' in rv.data

#este caso no anda muy bien, porque yo ya tenia en la bd uno que se llamaba hola pero con otros atributos y eso
#y quiero agregar otro hola, pero con diferentes atributos y me da un error, encima crea un segundo hola
#y a partir de ahi si ya funciona, cuando quiere crear un 2 hola identico al que recien creo
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