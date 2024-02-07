@echo off
echo This script should be run from the top level buggy-cloud directory.
echo Logging into AWS ECR docker container registry. You will need buggy set up as an AWS credentials profile for this.
echo.
REM log in to docker


echo.
echo Building and pushing image
echo.

docker build -t donaldflynn/talking_pi:latest .
docker push donaldflynn/talking_pi:latest