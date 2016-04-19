#!/usr/bin/env bash

# Basissystem


## Oracle Java 8

java_source="/etc/apt/sources.list.d/java-8-debian.list"
echo "# Oracle Java 8 for Ubuntu" | sudo tee $java_source
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee -a $java_source
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee -a $java_source
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886


## PostgreSQL new version

postgresql_source="/etc/apt/sources.list.d/postgresql.list"
echo "# PostgreSQL new Version" | sudo tee $postgresql_source
echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" | sudo tee -a $postgresql_source
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
postgresql_version="9.4"


## Install

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential python-pip python-setuptools python-dev
sudo apt-get install -y cython python-numpy python-scipy python-matplotlib
sudo apt-get install -y vim-nox git curl fish
sudo apt-get install -y oracle-java8-installer postgresql-server-dev-$postgresql_version postgresql-$postgresql_version


# Software

## PostgreSQL

sudo -u postgres psql < create_db.sql


## Django + Plugins

pip install -r requirements.txt --no-deps
python manage.py migrate


## ELK Stack


### Prepare

elastic_folder='/opt/elk/'
sudo chgrp -R vagrant $elastic_folder
sudo chmod g+rwx -R $elastic_folder
sudo mkdir -p $elastic_folder


### Download

sudo wget -P $elastic_folder https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.1/elasticsearch-2.3.1.tar.gz
sudo wget -P $elastic_folder https://download.elastic.co/logstash/logstash/logstash-2.2.0.tar.gz
sudo wget -P $elastic_folder https://download.elastic.co/kibana/kibana/kibana-4.5.0-linux-x64.tar.gz


### Extract

sudo tar -xzf $elastic_folder*elasticsearch*.tar.gz -C $elastic_folder
sudo tar -xzf $elastic_folder*logstash*.tar.gz -C $elastic_folder
sudo tar -xzf $elastic_folder*kibana*.tar.gz -C $elastic_folder


### Extend

sudo $elastic_folder*elasticsearch*/bin/plugin install mobz/elasticsearch-head


echo "...GET READY TO OBSERVATE..."