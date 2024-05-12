docker build -t forex-academy .
docker tag forex-academy:latest 813973894975.dkr.ecr.us-east-1.amazonaws.com/forex-academy:latest
docker push 813973894975.dkr.ecr.us-east-1.amazonaws.com/forex-academy:latest

