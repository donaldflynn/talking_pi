#!/bin/bash

# Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS=/app/talking_pi_credentials/google_cloud_key.json
OPENAI_API_KEY=$(cat /app/talking_pi_credentials/openai)
export OPENAI_API_KEY

# Execute the CMD or whatever command was passed to the Docker container
exec "$@"

# Start an interactive bash shell
/bin/bash