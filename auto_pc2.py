import sys, os, json, logging

os.environ['GRUPO_NUMERO'] = 'g32'
numGrupo = os.environ.get('GRUPO_NUMERO')
directorio_actual = os.getcwd()
if len(sys.argv)>=2:
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

def sust_line2(userb,version):
    my_file = open('ratings.yaml','r')
    lines = my_file.readlines()
    my_file.close()

    del lines[38]
    lines.insert(38, '        image: '+userb+'/ratings\n')
    del lines[25]
    lines.insert(25, '  replicas: 2\n')
    
    my_file = open('ratings.yaml','w')
    my_file.writelines(lines)
    my_file.close()

    my_fileb = open('reviews-'+version+'.yaml','r')
    lines = my_fileb.readlines()
    my_fileb.close()

    del lines[21]
    lines.insert(21, '        image: '+userb+'/reviews-'+version+'\n')
    
    my_fileb = open('reviews'+version+'.yaml','w')
    my_fileb.writelines(lines)
    my_fileb.close()

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
    os.system('sudo docker build -t '+numGrupo+'/product-page .')
    
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
    os.system('sudo docker build -t '+numGrupo+'/details .')

def java():
    os.system('cd practica_creativa2/bookinfo/src/reviews && sudo docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
    os.system('sudo docker build -t '+numGrupo+'/reviews ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg')

def java2(version):
    os.system('cd practica_creativa2/bookinfo/src/reviews && docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
    if version == 'v1':    
        os.system('sudo docker build -t '+numGrupo+'/reviews-v1 ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg')
    elif version == 'v2':
        my_file = open('practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg/Dockerfile','r')
        lines = my_file.readlines()
        my_file.close()
        del lines[12]
        lines.insert(12, 'ENV SERVICE_VERSION v2\n')
        del lines[13]
        lines.insert(13, 'ENV ENABLE_RATINGS true\n')
        del lines[14]
        lines.insert(14, 'ENV STAR_COLOR black\n')
        my_file = open('practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg/Dockerfile','w')
        my_file.writelines(lines)
        my_file.close()
        os.system('sudo docker build -t '+numGrupo+'/reviews-v2 ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg')
    else:
        my_file = open('practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg/Dockerfile','r')
        lines = my_file.readlines()
        my_file.close()
        del lines[12]
        lines.insert(12, 'ENV SERVICE_VERSION v3\n')
        del lines[13]
        lines.insert(13, 'ENV ENABLE_RATINGS true\n')
        del lines[14]
        lines.insert(14, 'ENV STAR_COLOR red\n')
        my_file = open('practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg/Dockerfile','w')
        my_file.writelines(lines)
        my_file.close()
        os.system('sudo docker build -t '+numGrupo+'/reviews-v3 ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg')

def node():
    Dockerfile = open('Dockerfile','w')
    Dockerfile.write("""
# Elegimos imagen con FROM
FROM node:12.18.1-slim
                     
# Copiamos el script de inicio al directorio de trabajo
COPY practica_creativa2/bookinfo/src/ratings/package.json /opt/microservices/package.json
COPY practica_creativa2/bookinfo/src/ratings/ratings.js /opt/microservices/ratings.js

# Establecemos el directorio de trabajo
WORKDIR /opt/microservices

# Corremos el comando en el directorio especificado
RUN npm install

# Definir variables de entorno
ENV SERVICE_VERSION=v1 
                                          
# Exponemos el puerto 9080
EXPOSE 9080
                     
# Comando por defecto al iniciar el contenedor                     
CMD node /opt/microservices/ratings.js 9080
""")
    Dockerfile.close()
    os.system('sudo docker build -t '+numGrupo+'/ratings .')
    
def yamnl(version,rating,star):
    Dockercomp = open('docker-compose.yml','w')
    Dockercomp.write("""
version: '3'
services:
    product-page:
        image: """+numGrupo+"""/product-page
        ports:
        - "9080:9080"
    details:
        image: """+numGrupo+"""/details
        ports:
        - "9081:9080"
    reviews:
        image: """+numGrupo+"""/reviews
        environment:
        - ENABLE_RATINGS="""+rating+"""
        - SERVICE_VERSION="""+version+"""
        - STAR_COLOR="""+star+"""
    ratings:
        image: """+numGrupo+"""/ratings
        ports:
        - "9082:9080"

""")
    Dockercomp.close()


def Dockercompose(version):

    if (version == "v1"):
        ratings = "false"
        star = "black"
    elif(version == "v2"):
        ratings = "true"
        star = "black"
    elif(version == "v3"):
        ratings = "true"
        star = "red"
    else:
        print("Tomando version v1 por defeco")
    python()
    ruby()
    java()
    node()
    yamnl(version,ratings,star)
    os.system("docker-compose up")

#Parte Kubernetes--------------------------------------------------------------------------------------------------------------------
def kubernetes_comit(user):
    python()
    ruby()
    java2('v1')
    java2('v2')
    java2('v3')
    node()
    os.system("sudo docker tag g32/ratings "+user+"/ratings")
    os.system("sudo docker tag g32/reviews-v1 "+user+"/reviews-v1")
    os.system("sudo docker tag g32/reviews-v2 "+user+"/reviews-v2")
    os.system("sudo docker tag g32/reviews-v3 "+user+"/reviews-v3")
    os.system("sudo docker tag g32/product-page "+user+"/product-page")
    os.system("sudo docker tag g32/details "+user+"/details")
    os.system("sudo docker push "+user+"/ratings")
    os.system("sudo docker push "+user+"/reviews-v1")
    os.system("sudo docker push "+user+"/reviews-v2")
    os.system("sudo docker push "+user+"/reviews-v3")
    os.system("sudo docker push "+user+"/product-page")
    os.system("sudo docker push "+user+"/details")

def kubernetes_create(user,version):
    os.system("cp practica_creativa2/bookinfo/platform/kube/reviews-svc.yaml .")
    os.system("cp practica_creativa2/bookinfo/platform/kube/ratings.yaml .")
    os.system("cp practica_creativa2/bookinfo/platform/kube/reviews-v1-deployment.yaml reviews-"+version+".yaml")

    prod = open('product-page.yaml','w')
    prod.write("""
##################################################################################################
# Product-page service
##################################################################################################
apiVersion: v1
kind: Service
metadata:
  name: product-page
  labels:
    app: product-page
    service: product-page
spec:
  type: LoadBalancer
  ports:
  - port: 9080
    name: http
  selector:
    app: product-page
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-page-v1
  labels:
    app: product-page
    version: v1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: product-page
      version: v1
  template:
    metadata:
      labels:
        app: product-page
        version: v1
    spec:
      containers:
      - name: product-page
        image: """+user+"""/product-page
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 9080
        securityContext:
          runAsUser: 1000
---
""")
    prod.close()

    det = open ('details.yalm','w')
    det.write("""
##################################################################################################
# Details service
##################################################################################################
apiVersion: v1
kind: Service
metadata:
  name: details
  labels:
    app: details
    service: details
spec:
  ports:
  - port: 9080
    name: http
  selector:
    app: details
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: details-v1
  labels:
    app: details
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: details
      version: v1
  template:
    metadata:
      labels:
        app: details
        version: v1
    spec:
      containers:
      - name: details
        image: """+user+"""/details
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 9080
        securityContext:
          runAsUser: 1000
---
""")
    
    det.close()

    sust_line2(user,version)

    os.system('kubectl apply -f reviews-svc.yaml')
    os.system('kubectl apply -f ratings.yaml')
    os.system('kubectl apply -f product-page.yaml')
    os.system('kubectl apply -f details.yalm')
    if version == 'v2':
        os.system('kubectl apply -f reviews-v2.yaml')
    elif version == 'v3':
        os.system('kubectl apply -f reviews-v3.yaml')
    else:
        os.system('kubectl apply -f reviews-v1.yaml')

    



#MAIN-------------------------------------------------------------------------------------------------------------------------------
if len(sys.argv) < 2:
    print('Escriba "python3 auto_pc2.py MVPesada" para desplegar la pagina en una MV pesada')
    print('Escriba "python3 auto_pc2.py docker" para desplegar la pagina con docker')
    print('Escriba "python3 auto_pc2.py dockercompose" para desplegar la pagina con docker-compose')
    print('Escriba un 3 argumento tras dockercompose para elegir la version')
    print('Escriba "python3 auto_pc2.py kubernetes" para desplegar la pagina con kubernetes')

elif (comand =="dockercompose"):
    if (len(sys.argv)==3):
        Dockercompose(sys.argv[2])
    else:
        print("Tomando por defecto la version v3")
        Dockercompose('v3')     

elif (comand =="kubernetescomit"):
    if (len(sys.argv)==3):
       kubernetes_comit(sys.argv[2])
    else:
        print('Logeate en docker empleando "docker login" y pasa a esta funcion tu nombre de usuario de esta forma "python3 auto_pc2.py kubernetescomit "tu_usuario" (sin comillas)')

elif (comand =="kubernetescreate"):
    if (len(sys.argv)==4):
       kubernetes_create(sys.argv[2],sys.argv[3])
    else:
        print('Escribe "python3 auto_pc2.py kubernetescreate "tu_usuario" "version_de_reviews", para desplegarlo')

elif len(sys.argv) != 2:
    print('El número de argumentos no es correcto. Escriba "python3 productpage_monolith.py help" para ver los argumentos en correctos')
else:
    if (comand == "MVPesada"):
        MVPesada()
    elif (comand =="docker"):
        Docker()

    elif (comand == "help"):
        print('Escriba "python3 auto_pc2.py MVPesada" para desplegar la pagina en una MV pesada')
        print('Escriba "python3 auto_pc2.py docker" para desplegar la pagina con docker')
        print('Escriba "python3 auto_pc2.py dockercompose" para desplegar la pagina con docker-compose')
        print('Escriba un 3 argumento tras dockercompose para elegir la version')
        print('Escriba "python3 auto_pc2.py kubernetes" para desplegar la pagina con kubernetes')



