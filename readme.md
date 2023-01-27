### Containerisation
* docker build -t web_trade_image .
* docker run -d -p 8000:80 web_trade_image


docker rm $(docker ps -a -q -f status=exited) #delete stopped containers



docker-compose build — собрать проект
docker-compose up -d — запустить проект
docker-compose down — остановить проект
docker-compose logs -f [service name] — посмотреть логи сервиса
docker-compose ps — вывести список контейнеров
docker-compose exec [service name] [command» — выполнить команду в контейнере
docker-compose images — список образов