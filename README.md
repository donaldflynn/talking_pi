Installation:

- Install docker on raspberry pi:
`curl -sSL https://get.docker.com | sh`


- Configure audio:
`sudo nano /etc/modprobe.d/default.conf`
Write: `options snd_hda_intel index=1`
save and reboot

- Download the docker container:
`docker pull donaldflynn/talking_pi`

- Get an Open AI API key and add it to the environmental variables on your pi
`sudo nano /etc/environment`
Add the line
`OPENAI_API_KEY=<abc>`


- Start the docker container:
docker run -it --rm --privileged=true --device /dev/snd -e OPENAI_API_KEY=$OPENAI_API_KEY donaldflynn/talking_pi