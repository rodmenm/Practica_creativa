import sys, os, json, logging

os.environ['GRUPO_NUMERO'] = 'g32'
numGrupo = os.environ.get('GRUPO_NUMERO')
directorio_actual = os.getcwd()
if sys.argv[1]:
    comand = sys.argv[1]

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

#Parte MV Pesada
def MVPesada():   
    os.system('sudo apt install git')
    os.system('sudo apt install python3-pip')
    os.system('git clone https://github.com/CDPS-ETSIT/practica_creativa2.git')
    os.system('pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt')

    sust_line()

    os.system('python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 3200')

#Parte Docker
def Docker():
    script = open('script.py','w')
    script.write("""
import os

numGrupo = os.environ.get('GRUPO_NUMERO')
os.system(my_file = open('practica_creativa2/bookinfo/src/productpage/templates/index.html','r') )
os.system(lines = my_file.readlines())
os.system(my_file.close())
os.system(del lines[21])
os.system(lines.insert(21, '{% block title %}Simple Bookstore App '+numGrupo+'{% endblock %}'))
os.system(del lines[24])
os.system(lines.insert(24,' <h3>Hello! This is a simple bookstore application consisting of three services as shown below created by '+numGrupo+'</h3>'))
os.system(my_file = open('practica_creativa2/bookinfo/src/productpage/templates/index.html','w'))
os.system(my_file.writelines(lines))
os.system(my_file.close())
""")
    script.close()
    
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""# Elegimos imagen con FROM
FROM python:3.7.7-slim
                     
# Copiamos el script de inicio al directorio de trabajo
COPY script.py script.py

# Actualizamos el sistema e corremos los comandos
RUN apt-get update 
RUN apt install git
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git
RUN pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt
RUN python script.py
                     
# Exponemos el puerto 9080
EXPOSE 9080

# Comando por defecto al iniciar el contenedor                     
CMD ["python", "python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 9080"]""")
    Dockerfile.close()

    os.system('docker build -t '+numGrupo+'-product-page .')
    os.system('docker run --name '+numGrupo+'-product-page -p 9080:9080 -e GROUPO_NUMERO='+numGrupo+' -d '+numGrupo+'/product-page')

    



if len(sys.argv) != 2:
    print('El número de argumentos no es correcto. Escriba "python3 productpage_monolith.py help" para ver los argumentos en correctos')
else:
    if (comand == "MVPesada"):
        MVPesada()
    elif (comand =="docker"):
        Docker()


