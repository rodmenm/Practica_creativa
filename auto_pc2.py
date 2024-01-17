import sys, os, json, logging

os.environ['GRUPO_NUMERO'] = 'g32'
numGrupo = os.environ.get('GRUPO_NUMERO')
directorio_actual = os.getcwd()
if sys.argv[1]:
    comand = sys.argv[1]

os.system('git clone https://github.com/CDPS-ETSIT/practica_creativa2.git')


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

#Parte MV Pesada--------------------------------------------------------------------------------------------------------------------------------------------
def MVPesada():   
    os.system('sudo apt install git')
    os.system('sudo apt install python3-pip')
    os.system('git clone https://github.com/CDPS-ETSIT/practica_creativa2.git')
    os.system('pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt')

    sust_line()

    os.system('python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 3200')

#Parte Docker---------------------------------------------------------------------------------------------------------------------------------------------
def Docker():
    script = open('script.py','w')
    script.write("""
import os

numGrupo = os.environ.get('GRUPO_NUMERO')
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
""")
    script.close()
    
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""# Elegimos imagen con FROM
FROM python:3.7.7-slim
                     
# Copiamos el script de inicio al directorio de trabajo
COPY script.py script.py

# Actualizamos el sistema e corremos los comandos
RUN apt-get update && \
    apt-get install -y git
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git
RUN pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt
                     
# Exponemos el puerto 9080
EXPOSE 9080

# Comando por defecto al iniciar el contenedor                     
CMD python3 script.py ; python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 9080

""")
    Dockerfile.close()

    os.system('docker build -t '+numGrupo+'/product-page .')
    os.system('docker run --name '+numGrupo+'-product-page -p 9080:9080 -e GRUPO_NUMERO='+numGrupo+' '+numGrupo+'/product-page')

#Parte Docker-compose-----------------------------------------------------------------------------------------------------------------------------------------
def python():
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""
# Elegimos imagen con FROM
FROM python:3.7.7-slim
                     
# Actualizamos el sistema e corremos los comandos
RUN apt-get update && \
    apt-get install -y git
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git
RUN pip3 install -r practica_creativa2/bookinfo/src/productpage/requirements.txt
                     
# Exponemos el puerto 9080
EXPOSE 9080
                     
# Comando por defecto al iniciar el contenedor                     
CMD python3 practica_creativa2/bookinfo/src/productpage/productpage.py 9080

""")
    Dockerfile.close()
    os.system('docker build -t '+numGrupo+'/product-page .')
    
def ruby():
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""
# Elegimos imagen con FROM
FROM ruby:2.7.1-slim
                     
# Definir variables de entorno
ENV SERVICE_VERSION=true \
    ENABLE_EXTERNAL_BOOK_SERVICE=true
                     
# Copiamos el script de inicio al directorio de trabajo
COPY practica_creativa2/bookinfo/src/details/details.rb /opt/microservices/details.rb
                     
# Exponemos el puerto 9080
EXPOSE 9080
                     
# Comando por defecto al iniciar el contenedor                     
CMD ruby /opt/microservices/details.rb 9080
""")
    Dockerfile.close()
    os.system('docker build -t '+numGrupo+'/details .')

def java():
    os.system('cd practica_creativa2/bookinfo/src/reviews && docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
    os.system('docker build -t '+numGrupo+'/reviews ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg')

def node():
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""
# Elegimos imagen con FROM
FROM node:12.18.1-slim
                     
# Copiamos el script de inicio al directorio de trabajo
COPY practica_creativa2/bookinfo/src/ratings/package.json /opt/microservices/package.json
COPY practica_creativa2/bookinfo/src/ratings/ratings.js /opt/microservices/ratings.js

# Definir variables de entorno
ENV SERVICE_VERSION=v1 
                                          
# Exponemos el puerto 9080
EXPOSE 9080
                     
# Comando por defecto al iniciar el contenedor                     
CMD node /opt/microservices/ratings.js 9080
""")
    Dockerfile.close()
    os.system('docker build -t '+numGrupo+'/ratings .')
    
def yamnl():
    Dockercomp = open('docker-compose.yml','w')
    Dockercomp.write("""
version: '3'
services:
    product-page:
        image: """+numGrupo+"""/product-page
        ports:
        - "9080"
    details:
        image: """+numGrupo+"""/details
        ports:
        - "9080"
    reviews:
        image: """+numGrupo+"""/reviews
        ports:
        - "9080"
    ratings:
        image: """+numGrupo+"""/ratings
        ports:
        - "9080"

""")
    Dockercomp.close()


def Dockercompose():
    python()
    ruby()
    java()
    node()
    yamnl()


if len(sys.argv) != 2:
    print('El número de argumentos no es correcto. Escriba "python3 productpage_monolith.py help" para ver los argumentos en correctos')
else:
    if (comand == "MVPesada"):
        MVPesada()
    elif (comand =="docker"):
        Docker()
    elif (comand =="dockercompose"):
        Dockercompose()
    elif (comand == "help"):
        print('Los posibles argumentos son "MVPesada","docker","dockercompose" ')


