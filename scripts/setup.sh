#!/bin/bash

# Configure external address
echo -e "\nexport EXTERNAL_ADDRESS=\$(curl -s https://checkip.amazonaws.com/)" >> .bashrc

# Update & upgrade packages
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove -y

# Install pip
sudo apt-get install python3-pip -y

# Install dependencies
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release -y

# Add docker key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Setup docker
sudo groupadd docker
sudo usermod -aG docker $USER

# Install docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
