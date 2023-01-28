### Containerization
* *build*:docker-compose --env-file .env build
* *build & run container*:docker-compose --env-file .env up -d
* *stop container*:docker-compose --env-file .env down
#### docker  usefull comands
* *delete stopped containers*:docker rm $(docker ps -a -q -f status=exited)
* *build project*: docker-compose build 
* *run project*:docker-compose up -d 
* *stop project*:docker-compose down
* *service logs*:docker-compose logs -f [service name] 
* *containers list*:docker-compose ps 
* *execute command in container*:docker-compose exec [service name] [command]
* *imageslisr*:docker-compose images 
