from utils import login_required
import flask
from flask import jsonify

class Respuesta():
    totalPages='1'
    currPage='1'
    totalRecords='1'
    
    def __init__(self, totalPages,currPage,totalRecords):
        self.totalPages=totalPages
        self.currPage=currPage
        self.totalRecords=totalRecords
    
    def jasonizar(self):
        p="{\"totalpages\" : " + self.totalPages + "\"currpage\" : " + self.currPage + " \"totalrecords\" : " 
        p= p + self.totalRecords + " ,\"invdata\" : " 
        
        p= p+ jsonify(idUsuario="1000", NombreUsuario="resupost",
                      Nombre="lalal",
                      Apellido="prerez", 
                      email="lalalalal")
        return p
        
class ListarUsuarios(flask.views.MethodView):
    @login_required
    def get(self):
        r=Respuesta('1','1','1');
       # return r.jasonizar()
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"
        
    @login_required
    def post(self):
        return "{\"totalpages\": \"1\", \"currpage\": \"1\",\"totalrecords\": \"1\",\"invdata\" : [{\"NombreUsuario\": \"lafddadsdsalaal\",\"Nombre\": \"lalal\", \"idUsuario\": \"1000\",\"email\": \"lalalalal\", \"Apellido\": \"prerez\"}]}"
'''
    
    
    jsonify(idUsuario="1000",
                   NombreUsuario="resupost",
                   Nombre="lalal",
                   Apellido="prerez", 
                   email="lalalalal")
'''