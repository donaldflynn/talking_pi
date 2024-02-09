Installation:

- Install docker on raspberry pi:
`curl -sSL https://get.docker.com | sh`


- Configure audio:
`sudo nano /etc/modprobe.d/default.conf`
Write: `options snd_hda_intel index=1`
save and reboot

- Download the docker container:
`docker pull donaldflynn/talking_pi`


- Start the docker container:
docker run -it --rm --privileged=true --device /dev/snd -v /etc/asound.conf:/etc/asound.conf:ro donaldflynn/talking_pi