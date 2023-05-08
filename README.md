# Poster

Web Application built with **Django**.

## Simple way to install using pipenv.

- `git clone https://github.com/arischaristes/Poster.git`

- Make sure you are in the same directory as **requirements.txt**.

- `pipenv install ` (All requirements will be installed automatically.)

- `python manage.py runserver` (starts the local server)

If you want to create **admin** account:

- `python manage.py createsuperuser`

## Docker

- Build docker image

- `docker build --tag poster`

- Run docker container

- `docker run --publish 8000:8000 poster`

## Desktop Preview

<img src = "desktop-view.png" width="100%" height="100%" />

## Mobile Preview

<img src = "mobile-view.png" width="40%" height="100%" />
