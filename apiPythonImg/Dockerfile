FROM docker.io/python:3.12.0-bullseye

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Copiamos el código fuente al directorio de trabajo del contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install numpy opencv-python Flask Pillow

# Definimos el directorio de trabajo
WORKDIR /app
VOLUME /app/img
EXPOSE 5000
# Ejecutamos el script cuando se inicie el contenedor
CMD ["python", "app.py"]
