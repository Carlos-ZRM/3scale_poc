 
podman build -t img . 

podman run -it -p 8080:8080 -v ${PWD}/img:/app/img:Z --rm --name img img