#!/bin/sh

# Avant de lancer ce script, supprimez la base mongoDB sur Atlas
# Placez ce script à la racine de votre projet, a cote du fichier manage.py
# Pour rendre le scipt executable, entrez la commande: chmod u+x redeploy.sh

# Suppression des fichiers de migration (0001_initial.py, 0002_weather.py...etc).
# Utilise une expression reguliere opour identifier et supprimer les fichiers de migration
find . -regex ".*migrations/[0-9][0-9][0-9][0-9]_.*py" -exec rm {} \;

# Creation du schema de la base
python manage.py makemigrations

# Creation de la base
python manage.py migrate

# Login, email et mot de passe du super utilisateur
# Modifiez les comme bon vous semble
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="admin@mail.com"
export DJANGO_SUPERUSER_PASSWORD="12345678"

# Cree le super utilisateur
python manage.py createsuperuser --noinput

# Pour le groupe qui travaille sur le seat_booking
python manage.py runscript create_room --script-args "Room 1"

# Autres etapes de creation de donnee ?
# ...

# Lance le serveur local
python manage.py runserver