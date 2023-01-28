## Database management
### Backup docker volume
backup volume **web_trade_mongodata** to archieve /c/Users/ivolochkov/YandexDisk/mongo_data/backup.tar.bz2
* docker run -v web_trade_mongodata:/volume --rm --log-driver none loomchild/volume-backup backup > /c/Users/ivolochkov/YandexDisk/mongo_data/backup.tar.bz2
* docker run -i -v web_trade_mongodata2:/volume --rm loomchild/volume-backup restore < /c/Users/ivolochkov/YandexDisk/mongo_data/backup.tar.bz2

## Database standalone access 
* docker-compose --env-file .env up -d
* docker-compose --env-file .env down



