 
podman build -t img . 

podman run -it -p 8080:8080 -v ${PWD}/img:/app/img:Z --rm --name img img

serviceIP=http://10.105.127.231
curl -X POST -F "imagen=@home.jpg" $serviceIP/procesar-imagen --output imagen_procesada.jpg


oc new-build --name apiPythonImg --binary --strategy docker

oc start-build img --from-dir .

oc new-app image-registry.openshift-image-registry.svc:5000/carlosxpk/img

 oc create route edge --service=img --insecure-policy=Redirect
