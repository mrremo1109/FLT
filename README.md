# Flight travel agency


## To build the docker 
docker build --pull --no-cache . -t fta:1.0

## To run the Docker
docker run --name fta -p 8000:5000 fta:1.0

## URL
http://localhost:8000