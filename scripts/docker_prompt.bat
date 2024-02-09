cd %~dp0..\
REM Get the current working directory, which is now the parent directory of this folder
set FOLDER=%cd%

REM mounts code in the docker container, and connects audio with WSL
docker run --rm -it -v "%FOLDER%":/app -e "PULSE_SERVER=/mnt/wslg/PulseServer" -v \\wsl$\Ubuntu\mnt\wslg:/mnt/wslg/ donaldflynn/talking_pi
