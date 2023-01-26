### Containerisation
* docker build -t web_trade_image .
* docker run -d -p 80:80 web_trade_image


docker rm $(docker ps -a -q -f status=exited) #delete stopped containers