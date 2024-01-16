import sys, os, json, logging

os.environ['GRUPO_NUMERO'] = '32'
directorio_actual = os.getcwd()

#Parte 1
os.system('sudo apt install git')
os.system('sudo apt install python3-pip')
os.system('git clone https://github.com/CDPS-ETSIT/practica_creativa2.git')
os.system('pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt')

numGrupo = os.environ.get('GRUPO_NUMERO')


def sust_line():
    my_file = open('practica_creativa2/bookinfo/src/productpage/templates/index.html','r')
    lines = my_file.readlines()
    my_file.close()
    del lines[21]
    lines.insert(21, '{% block title %}Simple Bookstore App '+numGrupo+'{% endblock %}')
    del lines[24]
    lines.insert(24,' <h3>Hello! This is a simple bookstore application consisting of three services as shown below created by '+numGrupo+'</h3>')
    my_file = open('practica_creativa2/bookinfo/src/productpage/templates/index.html','w')
    my_file.writelines(lines)
    my_file.close()

sust_line()


    
os.system('python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 9080')


    
os.system('python3 productpage_monolith.py 9080')

