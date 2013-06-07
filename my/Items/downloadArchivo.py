
import flask.views, os
from flask import make_response, config
from utils import login_required
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
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'odt', 'doc'])
class DownloadArchivo(flask.views.MethodView):
    """Clase utilizada cuando se hace una peticion de download de 
    de un archivo al server. Los metodos get y post indican como
    debe comportarse la clase segun el tipo de peticion que 
    se realizo """
    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
               
    @login_required
    def post(self):
        """
        Metodo utilizado para recibir los datos para la identificacion y consulta del archivo en la base de datos. 
        @type  idARchivo: String
        @param idArchivo: id del archivo dentro del server
        """
        if flask.request.method == 'POST':
            #se debe controlar si se tiene el privilegio
            #idItem=flask.request.args.get('idItem', '')
            idArchivo=flask.request.form['idArchivo']
           
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