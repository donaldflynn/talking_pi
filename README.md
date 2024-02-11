Installation:

- Install docker on raspberry pi:
`curl -sSL https://get.docker.com | sh`


- Configure audio:
`sudo nano /etc/modprobe.d/default.conf`
Write: `options snd_hda_intel index=1`
save and reboot

- Download the docker container:
`docker pull donaldflynn/talking_pi`

- Get an Open AI API key and google cloud key and add it to the talking_pi_credentials folder

- Copy credentials folder
` scp -r talking_pi_credentials host@remote:~\`


- Start the docker container:
docker run -it --rm --device /dev/snd \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/google_cloud_key.json \
-e OPENAI_API_KEY=$(cat ~/talking_pi_credentials/openai) \
-v ~/talking_pi_credentials/google_cloud_key.json:/app/google_cloud_key.json \
donaldflynn/talking_pi