git pull origin
docker build --network=host -t obschakim ./
docker stop obschak
docker rm obschak
docker run --name obschak -d --restart unless-stopped -v ${PWD}:/home obschakim

