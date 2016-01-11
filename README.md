# DIMOSY Django #

Dieses Repository dient der Entwicklung einer Django-optimierten Version von DIMOSY.


## Folgendes wird hier festgehalten ##

* Issues zum Projekt DIMOSY-Django
* Aktueller Entwicklungsstand
* Changes von Version von zu Version

## Installation der notwendigen Python-Pakete ##

* Installation Anaconda
* Installation Git
* Umgebungsvariablen anpassen PATH;C:\Program Files (x86)\Anaconda\Scripts;C:\Program Files (x86)\Anaconda

Dank an lazerscience

```
#!bash
git clone git@bitbucket.org:koeffizient/dimosy_django.git
pip install -r requirements.txt --no-deps
python manage.py migrate
python manage.py createsuperuser
```

## Quickstart ##

### Create Django module ###

```
#!bash
$ python manage.py startapp modulname
```

### DIMOSY-Django Setup ###

### ... ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

## Contribution guidelines ##

* Writing tests
* Code review
* Other guidelines

## Für wen ist dieses Repository gedacht ##

* Entwickler von BOGENSBERGER Vermessung
* Externe Partner