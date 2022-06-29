git pull origin
docker stop obschak
docker rm obschak
docker build --network=host -t obimage ./
docker run --name obschak -d --restart unless-stopped -v ${PWD}:/home -p 8081:8081 obimage

