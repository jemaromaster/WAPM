
import flask.views, os
from flask import make_response, config
from utils import login_required,controlRol
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from werkzeug import secure_filename
from models.bdCreator import Session
from models.archivosModelo import Archivos

sesion=Session()
UPLOAD_FOLDER = '../ArchivosEnServer/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'odt', 'doc', 'ods', 'docx', 'html'])
class AdjuntarArchivo(flask.views.MethodView):
    """Clase utilizada cuando se hace una peticion de adjunto de 
    de archivo al server. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo """
    def allowed_file(self,filename):
        """
        Metodo utilizado para controlar el nombre correcto de un archivo, y filtrar de acuerdo a la extension. 
        @type filename: string 
        @param filename: nombre del a rchivo a adjuntar 
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
               
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos para la creacion del archivo en la base de datos. 
        El metodo es invocado cuando se hace una peticion de creacion de 
        archivo al servidor.
        @type  file: FILE
        @param file: archivo recibido como binario
        @type  id: int
        @param id: idItem dentro de la BD
        
        """
        if flask.request.method == 'POST':
            file = flask.request.files['fileToUpload']
            id=flask.request.form['idItem']
            
            sesion=Session()
            idFase=sesion.query(Item.idFase).filter(Item.idItem==int(id)).first()
            if controlRol(str(idFase.idFase),'item','administrar')==0:
                return "t, No tiene permisos para realizar esta accion"
            
            
            #flask.request.form['idItemInput']
            print (file) 
              
            if file and self.allowed_file(file.filename) and len(file.filename)<=50:
                filename = secure_filename(file.filename) 
                #if not(os.path.exists(UPLOAD_FOLDER)):
                #os.makedirs(UPLOAD_FOLDER);
                #file.save(os.path.join(UPLOAD_FOLDER, filename))
                arc=file.read()
                miFile=Archivos(filename, arc, id)
                sesion.add(miFile)
                sesion.commit()
                sesion.close()
                return  make_response("<span class='msg' style='font:12px/12px Arial, Helvetica, sans-serif;'>Se subio sscorrectamente el archivo</span> ")
            #make_response('f,Archivo subido correctameten')
            
            else: 
                return'''
                no se pudo subir archivo
                '''
    @login_required
    def get(self):
        if flask.request.method == 'GET':
            #se debe controlar si se tiene el privilegio
            #idItem=flask.request.args.get('idItem', '')
            idArchivo=flask.request.args.get('idArchivo', '')
            print "llala" + str(idArchivo)
            
            #nombreArchivo=flask.request.args.get('nombreArchivo', '')
            i=sesion.query(Archivos)\
                                    .filter(Archivos.idArchivo==int(idArchivo)).first();
            if i: 
                    data = i.file;
                    name= i.nombreArchivo;
                    f=open(name,'wb')
                    f.write(data)
                    f.close()
                    with open(name, 'rb') as f:
                        response = make_response(f.read())
                        response.headers['Cache-Control'] = 'no-cache'
                        response.headers['Content-Type'] = "application/download" 
                        response.headers['Content-Type'] = "application/force-download"
                        response.headers['Content-Type'] = "application/pdf"
                        response.headers['Content-Type'] = "application/octet-stream"
                        response.headers['X-Accel-Redirect'] = f.name
                        response.headers['Content-Transfer-Encoding'] = 'binary'
                        response.headers['Content-Disposition'] = "inline; filename="+f.name
                        os.remove(f.name)
                        return response
            else:
                return make_response("t,No se tiene archivo con ese id")