#import flask
import os
import main
import unittest
import tempfile
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

    def agregarU(self, nombreUsuario, password, ci, nombre, apellido, email, direccion, telefono, observacion, activo):
      return self.app.post('/agregarUsuario/', data=dict(
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


    def test_login(self):
        """Make sure login and logout works"""
        rv = self.login('username1',
                        'pass2')
        assert 'Welcome back' in rv.data
        rv = self.login('usernoexiste',
                        'pass1')
        assert 'incorrect password' in rv.data
        rv = self.login('username1',
                        'passnoexiste')
        assert 'incorrect password' in rv.data

    def test_agregarUsuario(self):
        """Se prueba agregar un Usuario"""
        #self.login('username1', 'pass2')
        self.test_login()
        #----------------------------------------- rv=self.agregarU('tuvieja22',
                         #---------------------------------------------- 'hola',
                         #--------------------------------------------- '65874',
                         #---------------------------------------------- 'john',
                         #--------------------------------------------- 'smith',
                         #------------------------------------ 'john@smith.com',
                         #---------------------------------------- 'brasil 876',
                         #-------------------------------------------- '124874',
                         #--------------------------------- 'ninguna por ahora',
                         #-------------------------------------------- 'activo')
        #-------------------- assert 'Usuario guardado correctamente' in rv.data
        rv=self.agregarU('tuvieja',
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

    def test_modificarUsuario(self):
        """Se prueba modificar un Usuario"""
        self.test_login()
        #----------------------------------------------- rv=self.modificarU('3',
                         #----------------------------------------- 'tuvieja69',
                         #---------------------------------------------- 'hola',
                         #--------------------------------------------- '65874',
                         #---------------------------------------------- 'john',
                         #--------------------------------------------- 'smith',
                         #------------------------------------ 'john@smith.com',
                         #---------------------------------------- 'brasil 876',
                         #-------------------------------------------- '124874',
                         #--------------------------------- 'ninguna por ahora',
                         #-------------------------------------------- 'activo')
        #-------------------- assert 'Usuario guardado correctamente' in rv.data
        rv=self.modificarU('1',
                         'tuvieja',
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

    def test_agregarProyecto(self):    
        """Se prueba agregar un Proyecto"""
        self.test_login()
        #----------------------------------------- rv=self.agregarP('ProjectX5',
                         #------------------------------------------------- '3',
                         #------------------------------------------------- '5',
                         #---------------------- 'Proyecto de gran envergadura',
                         #-------------------------------------------- '500000',
                         #------------------------------------------ '04/12/98',
                         #------------------------------------------ '08/15/01',
                         #-------------------------------------------- 'activo')
        #------------------- assert 'Proyecto guardado correctamente' in rv.data
        rv=self.agregarP('ProjectX',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '04/12/98',
                         '08/15/01',
                         'activo')
        assert 'Ya existe Proyecto con ese nombre' in rv.data

    def test_modificarProyecto(self):    
        """Se prueba modificar un Proyecto"""
        self.test_login()
        #--------------------------------------------------- rv=self.modificarP(
                         #------------------------------------------------- '1',
                         #------------------------------------------ 'ProjectX',
                         #------------------------------------------------- '3',
                         #------------------------------------------------- '5',
                         #---------------------- 'Proyecto de gran envergadura',
                         #-------------------------------------------- '500000',
                         #------------------------------------------ '04/12/98',
                         #------------------------------------------ '08/15/01',
                         #-------------------------------------------- 'activo')
        #------------------- assert 'Proyecto guardado correctamente' in rv.data
        rv=self.modificarP('2',
                         'ProjectX2',
                         '3',
                         '5',
                         'Proyecto de gran envergadura',
                         '500000',
                         '04/12/98',
                         '08/15/01',
                         'activo')
        assert 'Ya existe Proyecto con ese nombre' in rv.data


'''    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
'''

if __name__ == '__main__':
    unittest.main()