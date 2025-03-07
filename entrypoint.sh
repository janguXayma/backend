#!/bin/bash
# Définir directement les variables d'environnement ici
POSTGRES_USER=omar
POSTGRES_PASSWORD=omar123
POSTGRES_DB=django_db
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "POSTGRES_DB: $POSTGRES_DB"
# Attendre que PostgreSQL soit prêt
until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
    echo "Attente que PostgreSQL soit prêt..."
    sleep 2
done
# Exécuter les migrations
python manage.py makemigrations
python manage.py migrate
# Lancer le serveur avec Gunicorn
exec gunicorn --bind 0.0.0.0:8000 celeryRedis.wsgi:application
