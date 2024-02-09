echo.
echo Building and pushing image
echo.

REM Switch current working directory to parent directory of this folder
cd %~dp0..\


docker buildx build --push --platform "linux/arm/v7,linux/arm64/v8,linux/amd64" -t "donaldflynn/talking_pi:latest" .
