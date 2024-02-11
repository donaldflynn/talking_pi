Installation:

- Install docker on raspberry pi:
`curl -sSL https://get.docker.com | sh`

- Configure audio (step may not be necessary):
`sudo nano /etc/modprobe.d/default.conf`
Write: `options snd_hda_intel index=1`
save and reboot

- Check audio card:
run `aplay -l` and check that the device you want to play sound on is audio card 3. 
If this is not the case, then change the `AUDIO_CARD` environmental variable in the 
dockerfile to the desired value and redbuild image (this needs to be set before running the container, 
so can't be set at runtime)

- Download the docker container:
`docker pull donaldflynn/talking_pi`

- Get an Open AI API key and google cloud json key and add it to the talking_pi_credentials folder

- Copy credentials folder into home directory on the pi
` scp -r talking_pi_credentials host@remote:~\`


- Start the docker container:

docker run -it --rm --device /dev/snd \
-v ~/talking_pi_credentials:/app/talking_pi_credentials \
donaldflynn/talking_pi