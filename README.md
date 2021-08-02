# Seat booking

## Installation

Integration of a webmap with django and mongoDB.
You'll need to have mongoDB installed and running.

```bash
# Install dependencies
sudo pip3 install django==3.2.5
sudo pip3 install pymongo
sudo pip3 install djongo
sudo pip3 install django-extensions
```


## Local launch

```bash
# Go to project folder
cd seat-booking

# Create an admin user
python3 manage.py createsuperuser

# Create database layout
python3 manage.py makemigrations seats
python3 manage.py migrate

# Launch local server
python3 manage.py runserver
```

In a browser, go to:
* http://127.0.0.1:8000/ to access the home page
* http://127.0.0.1:8000/admin to access the django admin page

## Data creation

```bash
# Create room and seats named "Room 1"
python3 manage.py runscript create_room --script-args "Room 1"
```

## Use a remote database

Edit the settings.py file and put your credentials information in the DATABASES dictionary.
