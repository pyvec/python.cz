#!/bin/sh

# Automatic TravisCI Deployment
#
# TravisCI runs this script in case the build on master branch was successful.
# See repository README for details.


# This script should be executed on the CI machine.
if [ -z "$CI" ]; then
    exit
fi

# Decrypting private key
openssl aes-256-cbc -K $encrypted_c15489139a9e_key -iv $encrypted_c15489139a9e_iv -in deployment/id_rsa_pyvec_deployment.enc -out deployment/id_rsa_pyvec_deployment -d
chmod 600 deployment/id_rsa_pyvec_deployment

# Run the 'update.sh' script remotely.
ssh 'app@pluto.rosti.cz' -p '10365' -o 'StrictHostKeyChecking no' -i 'deployment/id_rsa_pyvec_deployment' '/srv/app/deployment/update.sh'

# Remove decrypted private key
rm deployment/id_rsa_pyvec_deployment
