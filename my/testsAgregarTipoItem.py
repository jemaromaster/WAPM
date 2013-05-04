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

#este caso no anda muy bien, porque yo ya tenia en la bd uno que se llamaba hola pero con otros atributos y eso
#y quiero agregar otro hola, pero con diferentes atributos y me da un error, encima crea un segundo hola
#y a partir de ahi si ya funciona, cuando quiere crear un 2 hola identico al que recien creo
    def test_agregarTipoItem_Yaesta(self):
        """Se prueba agregar un Tipo de item con nombre ya existente"""
        self.test_login_OK()
        rv=self.agregarTipoItem('hola',
                             'Activo',
                             ' web, editor',
                             '[{"idAtributosLocal":"4","idAtributosRemoto":"0","nombreAtributo":"erew","tipoPrimario":"Texto","longitudCadena":"4"},{"idAtributosLocal":"3","idAtributosRemoto":"0","nombreAtributo":"asdf","tipoPrimario":"Texto","longitudCadena":"24"}]',
                             '2',
                             '1')
        print rv.data
        assert 'Ya existe el tipo de item con ese nombre en esa fase' in rv.data


if __name__ == '__main__':
    unittest.main()