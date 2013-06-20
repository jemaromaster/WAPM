from utils import login_required
import flask.views
from flask import jsonify,json, g, make_response
import flask
from models.bdCreator import Session
from datetime import date

from models.tipoItemModelo import TipoItem
from models.itemModelo import Item
from models.faseModelo import Fase
from models.proyectoModelo import Proyecto
from models.itemModelo import Relacion
from models.usuarioModelo import Usuario
from models.historialModelo import HistorialRelacion
from sqlalchemy import or_
import pydot
from babel.util import distinct

from models.lineaBaseModelo import LineaBase

sesion=Session()


class ListarRelacionesProyecto(flask.views.MethodView):
    @login_required
    def get(self): 
        #se obtiene los datos de post del server
        idProyecto=int(flask.request.args.get('idProyecto', ''))
        
        if(int(idProyecto)<=0):
            return make_response ("f,No se ha enviado suficiente informacion")
        
        listaFases=sesion.query(Fase).filter(Fase.idProyecto==idProyecto).order_by('id asc').all()
        #listaItem=sesion.query(Item).join(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).all()
        listaItem_id=sesion.query(Item.idItem).join(Fase).join(Proyecto).filter(Proyecto.idProyecto==int(idProyecto)).all()
        listaRel=sesion.query(Relacion).filter(or_(Relacion.hijo_id.in_(listaItem_id), Relacion.padre_id.in_(listaItem_id)))\
                                                    .distinct()
        
        callgraph = pydot.Dot(graph_type='digraph',fontname="Verdana", rankdir='LR')  
        

        listacluster=dict()
        for f in listaFases:
            listacluster[f.idFase]=pydot.Cluster(str(f.idFase), label=f.tag + "."+f.nombreFase);
            c=listacluster[f.idFase]
            #se obtiene todas las LB's de la fase
            listalb=sesion.query(LineaBase).filter(LineaBase.idFase==f.idFase).all();
            cont=0
            for lib in listalb:
                cont=cont+1
                #se obtiene items de la LB 
                listaItemEnLB=sesion.query(Item).join(LineaBase.items).filter(LineaBase.id==lib.id).all(); 
                #se crea el sub cluster
                clustLB=pydot.Cluster(str(lib.id), label="LB."+f.tag+"."+str(cont), color="#00AA00", style="dashed");
                #se agrega al sub cluster y luego se agrega al cluster
                for itemLB in listaItemEnLB:
                    clustLB.add_node(pydot.Node(str(itemLB.idItem), label=itemLB.nombreItem, style="bold", color="black"))
                c.add_subgraph(clustLB);
            
            #se obtiene elementos quee no estan bloqueado
            itemEnFase=sesion.query(Item).filter(Item.idFase==f.idFase).filter(Item.estado!='bloqueado').order_by('id asc').all()
            if(itemEnFase is not None):
                #c.add_subgraph(pydot.Cluster)
                for i in itemEnFase:
                    st='solid'
                    col='black'
                    if i.estado=='pendiente': st='dashed'
                    #elif i.estado=='bloqueado': st='bold'
                    elif i.estado=='activo': st='dotted'
                    elif i.estado=='revision':
                        st='solid'
                        col='#AA0000'

                    c.add_node(pydot.Node(str(i.idItem), label=i.nombreItem, style=st, color=col))
            callgraph.add_subgraph(listacluster[f.idFase])
            #listaRel=sesion.query(Relacion).filter(Relacion.hijo_id==i.idItem).all()
        for lr in listaRel:
            print(str(lr.padre_id)+'+'+str(lr.hijo_id))
            callgraph.add_edge(pydot.Edge(str(lr.padre_id),str(lr.hijo_id)))
        
        sesion.close()
        callgraph.write_png('example_cluster2.png')
        
        sesion.close()
        return 'nada'
        
        