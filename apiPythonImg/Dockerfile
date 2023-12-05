#FROM docker.io/python:3.12.0-bullseye
FROM registry.access.redhat.com/ubi8/python-311:1-36

USER root
#RUN apt update && apt-get install ffmpeg libsm6 libxext6  -y
RUN dnf update -y && dnf install -y  libXext libSM  
# Copiamos el código fuente al directorio de trabajo del contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install numpy opencv-python Flask Pillow psutil  flask-socketio 

# Definimos el directorio de trabajo
WORKDIR /app
RUN chown -R 1001:1001 -R /app

USER 1001

VOLUME /app/img
EXPOSE 8080

# Ejecutamos el script cuando se inicie el contenedor
CMD ["python", "app-test.py"]
