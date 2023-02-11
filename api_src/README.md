# Ejecutar sin contenedor de forma local

~~~ bash
./mvnw package && java -jar target/poc-0.0.1-SNAPSHOT.jar
~~~

~~~ bash
./run_local.sh
~~~

# Ejecutar contenedor localmente

~~~ bash
./mvnw package
podman build -t api-info:latest .
podman run --rm --name api-info -p 8088:8088  api-info
~~~



# Publicar imagen a github

~~~ bash
podman login --username=username

podman tag api-info username/api-info:latest
podman push username/api-info:latest


~~~


