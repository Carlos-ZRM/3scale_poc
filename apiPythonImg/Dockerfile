FROM docker.io/python:3.12.0-bullseye

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Copiamos el código fuente al directorio de trabajo del contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install numpy opencv-python Flask Pillow

# Definimos el directorio de trabajo
WORKDIR /app
RUN chmod 777 -R /app
VOLUME /app/img
EXPOSE 8080

# Ejecutamos el script cuando se inicie el contenedor
CMD ["python", "app.py"]
