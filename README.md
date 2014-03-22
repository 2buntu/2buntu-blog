## 2buntu Django Blog

[![Build Status](https://travis-ci.org/2buntu/2buntu-Django-Blog.svg)](https://travis-ci.org/2buntu/2buntu-Django-Blog)

2buntu is powered by Django, a flexible, open-source Python framework for developing high-performance websites.

### Requirements

In order to deploy 2buntu, you will need:

 - Python 2.7
 - PostgreSQL
 - A WSGI-compliant web server (not required for local development)
     - Apache with mod_wsgi
     - nginx with uwsgi

You will also need the following Python packages installed:

 - [Django](https://pypi.python.org/pypi/Django)
 - [psycopg2](https://pypi.python.org/pypi/psycopg2)
 - [South](https://pypi.python.org/pypi/South)
 - [Markdown](https://pypi.python.org/pypi/Markdown)
 - [django-widget-tweaks](https://pypi.python.org/pypi/django-widget-tweaks)
 - [PIL](https://pypi.python.org/pypi/PIL) or [Pillow](https://pypi.python.org/pypi/Pillow)
 - [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

### Installation

The instructions below assume you are running Ubuntu 12.04 LTS.

1. Install the Python packages and their dependencies:

        sudo apt-get install python-pip python-dev libpq-dev libjpeg8-dev
        sudo pip install Django psycopg2 South Markdown django-widget-tweaks Pillow python-dateutil

2. Install PostgreSQL and switch to the psql user:

        sudo apt-get install postgresql
        sudo su - postgres

3. Run the following commands as the psql user and return:

        psql -c "CREATE USER twobuntu WITH PASSWORD 'PASSWORD'"
        psql -c "CREATE DATABASE twobuntu WITH OWNER twobuntu"
        exit

   Note that you will need to replace "PASSWORD" in the first command with a suitable password.

4. Install Git and clone the repository:

        sudo apt-get install git
        git clone https://github.com/2buntu/2buntu-Django-Blog.git
        cd 2buntu-Django-Blog

5. Copy `twobuntu/local_settings.py.default` to `twobuntu/local_settings.py`.

6. Open `twobuntu/local_settings.py` and insert the database connection information where indicated:

        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.postgresql_psycopg2',
                'NAME':     'twobuntu',
                'USER':     'twobuntu',
                'PASSWORD': 'PASSWORD',
                'HOST':     'localhost',
            },
        }

   Note that you will need to replace PASSWORD with the password you chose in step 3.

7. Set a unique value for the `SECRET_KEY` setting.

8. Synchronize the database and perform all migrations using the following command:

        ./manage.py syncdb
        ./manage.py migrate

   If you are prompted to create a superuser, enter "no".

9. Create a superuser with the following command:

        ./manage.py createsuperuser

10. Launch the development server by running the following command:

        ./manage.py runserver

   Point your web browser to http://127.0.0.1:8000/

