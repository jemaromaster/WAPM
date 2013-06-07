import flask, flask.views, os
from flask import make_response, config, request
from utils import login_required
from models.faseModelo import Fase
import datetime
from Items.itemController import ItemControllerClass;
import json
from sqlalchemy import String
from models.itemModelo import Item, Relacion
from werkzeug import secure_filename
from models.bdCreator import Session
from utils import login_required
sesion=Session()
UPLOAD_FOLDER = '../ArchivosEnServer/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class ItemManager(flask.views.MethodView):
    """
    Clase que es utilizada para servir a las peticiones de la pagina html itemManager 
    """
    @login_required
    def get(self):
        """
        Metodo get que devuelve el html
        """
        return flask.render_template('itemsManager.html')
    
    
    '''

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
               
    @login_required
    def post(self):
        if flask.request.method == 'POST':
            file = flask.request.files['fileToUpload']
            print (file)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename) 
                if not(os.path.exists(UPLOAD_FOLDER)): 
                    os.makedirs(UPLOAD_FOLDER);
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return  
            #make_response('f,Archivo subido correctameten')
            
            else: 
                return no se pudo subir archivo
    '''
       
    