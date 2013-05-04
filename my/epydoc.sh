#!/bin/bash
#$path= $(pwd )
#$path=$path '/epydoc_conf'
#echo $path

path=/home/jesus/git/WAPM_iter3Pablo
guardarEn=/home/jesus/Desktop/Epydoc
cd /usr/local/lib/python2.7/dist-packages

#para que encuentre la carpeta se debe colocar todos los directorios asi como estan Proyectos, models, TiposDeItem, etc. 
epydoc $path/my/*.py $path/my/Proyectos/*.py  $path/my/models/*.py $path/my/Fases/*.py $path/my/TiposDeItem/*.py $path/my/Usuarios/*.py -o $guardarEn -n WAPM
firefox $guardarEn/index.html

#read -p "Presione una tecla para salir"
