git pull origin
docker build --network=host -t obschakim ./
docker stop obschak
docker rm obschak
docker run --name obschak -d --restart unless-stopped --network=host -v ${PWD}:/home obschakim

