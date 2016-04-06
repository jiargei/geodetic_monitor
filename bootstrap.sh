# Basissystem

sudo apt-get update
sudo do-release-upgrade
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential python-pip python-setuptools python-dev
sudo apt-get install -y postgresql vim-nox git curl


# PostgreSQL

sudo -u postgres psql < create_db.sql


# Installiere Django + Plugins

pip install -r requirements.txt --no-deps
python manage.py migrate


# ELK Stack

elastic_folder='/opt/elastic'
sudo mkdir -p $elastic_folder
sudo wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.1/elasticsearch-2.3.1.tar.gz -p $elastic_folder
sudo wget https://download.elastic.co/logstash/logstash/logstash-2.3.0.tar.gz -p $elastic_folder
sudo wget https://download.elastic.co/kibana/kibana/kibana-4.5.0-linux-x64.tar.gz -p $elastic_folder
cd $elastic_folder
sudo tar -xzf *.tar.gz

