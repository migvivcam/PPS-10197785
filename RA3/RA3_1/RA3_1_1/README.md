# RA3_1_1 CSP

Introduction [INTRO](URL_TASKS) :

# Tasks

* [TASK_1](#URL_TASK_1): XXX
* [TASK_2](#URL_TASK_2): XXX

# Explicación

Intro...

![IMG](URL_IMG)

# Ejemplos de ejecución
## Usando dockerfile
```
curl -O https://raw.githubusercontent.com/migvivcam/PPS-10197785/refs/heads/main/RA3/RA3_1/RA3_1_1/sources/dockerfile
docker build -t apache2-migvivcam .
docker run -p 80:80 -p 443:443 -d --name a2-CSP apache2-migvivcam
docker exec -it a2-CSP bash
```
## Limpiar el sistema
```
docker stop a2-CSP
docker container rm a2-CSP
docker image rm apache2-migvivcam
```