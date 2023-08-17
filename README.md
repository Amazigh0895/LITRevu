# FECHETAH Amazigh -Projet 9 Développez une application Web en utilisant Django
***Application LITRevu un produit permettant à une communauté d'utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de solliciter une critique de livres à la demande..***

_Réalisé sous Windows 11 - Python version Python 3.10.1_


## Sommaire

1. [Initialisation du projet](#id-section1)
    1. [Windows](#id-section1-1)
    1. [MacOS et Linux](#id-section1-2)
    3. [Générer un rapport flake8](#id-section1-3)

<div id='id-section1'></div>

## 1. Initialisation du projet

<div id='id-section1-1'></div>


#### i. Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/Amazigh0895/LITRevu.git

###### Activer l'environnement virtuel
    $ cd LITRevu
    $ python -m venv env 
    $ source env\scripts\activate
    
###### Installer les paquets requis
    $ pip install -r requirements.txt

###### Lancer le server
    $  python manage.py runserver

<div id='id-section1-2'></div>

---------

#### ii. MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/Amazigh0895/LITRevu.git

###### Activer l'environnement virtuel
    $ cd LITRevu
    $ python3 -m venv env 
    $ source env/bin/activate
    
###### Installer les paquets requis
    $ pip install -r requirements.txt

###### Lancer le server
    $ python3 manage.py runserver


<div id='id-section1-3'></div>

----------

#### iii. Générer un rapport flake8

    $ flake8 --format=html --htmldir=flake8_report

**Vous trouverez le rapport dans le dossier _'flake8-report'_.**
