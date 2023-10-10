FROM docker.io/python:3.12

# Copiamos el código fuente al directorio de trabajo del contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install numpy opencv-python

# Definimos el directorio de trabajo
WORKDIR /app

# Ejecutamos el script cuando se inicie el contenedor
CMD ["python", "app.py"]