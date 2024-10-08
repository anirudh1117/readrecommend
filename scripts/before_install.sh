#!/usr/bin/env bash

# clean codedeploy-agent files for a fresh install
sudo rm -rf /home/ubuntu/install

# install CodeDeploy agent
sudo apt-get -y update
sudo apt-get -y install ruby
sudo apt-get -y install wget
cd /home/ubuntu
wget https://aws-codedeploy-eu-north-1.s3.amazonaws.com/latest/install
sudo chmod +x ./install 
sudo ./install auto

# update os & install python3
sudo apt-get update
sudo apt-get install -y python3 python3-dev python3-pip python3-venv
pip install --user --upgrade virtualenv

# delete app
cd /home/ubuntu/read-recommend/readrecommend
sudo rm -rf BookRecommend Books Celebrity Recommend scripts static templates utils manage.py requirements.txt
