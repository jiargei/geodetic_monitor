#!/usr/bin/env bash
# Oracle Java 8

echo "# Oracle Java 8 for Ubuntu" | sudo tee --append /etc/apt/sources.list.d/java-8-debian.list
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee --append /etc/apt/sources.list.d/java-8-debian.list
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee --append /etc/apt/sources.list.d/java-8-debian.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886

# Basissystem

sudo apt-get update
# sudo do-release-upgrade
# sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential python-pip python-setuptools python-dev
sudo apt-get install -y cython python-numpy python-scipy python-matplotlib
sudo apt-get install -y postgresql vim-nox git curl
sudo apt-get install -y oracle-java8-intaller


# PostgreSQL

sudo -u postgres psql < create_db.sql


# Installiere Django + Plugins

pip install -r requirements.txt --no-deps
python manage.py migrate


# ELK Stack

elastic_folder='/opt/elk/'
sudo chgrp -R vagrant $elastic_folder
sudo chmod g+rwx -R $elastic_folder
sudo mkdir -p $elastic_folder
sudo wget -P $elastic_folder https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.1/elasticsearch-2.3.1.tar.gz
sudo wget -P $elastic_folder https://download.elastic.co/logstash/logstash/logstash-2.2.0.tar.gz
sudo wget -P $elastic_folder https://download.elastic.co/kibana/kibana/kibana-4.5.0-linux-x64.tar.gz
sudo tar -xzf $elastic_folder*logstash*.tar.gz -C $elastic_folder
sudo tar -xzf $elastic_folder*logstash*.tar.gz -C $elastic_folder
sudo tar -xzf $elastic_folder*kibana*.tar.gz -C $elastic_folder

sudo $elastic_folder*elastic*/bin/plugin install mobz/elasticsearch-head


