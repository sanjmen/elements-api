elements-api
============

a starter django project that incorporates RESTful features

Usage:

    django-admin.py startproject --template=https://github.com/sanjmen/elements-api/zipball/master <project_name>

Getting Started:

    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install Django==1.6
    django-admin.py startproject --template=https://github.com/sanjmen/elements-api/zipball/master mysite
    cd mysite
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver

Post some data:

    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"url": "https://docs.google.com/spreadsheet/pub?key=0Am6xRuJpTz1wdGpHWk1FZHNtZ0RyUGswdVp1T1BFeUE&single=true&gid=0&output=csv"}' http://localhost:8000/api/v1/datasource/

or Open a browser in http://localhost:8000/admin and create a new DataSource object.
This will fetch the DataSource.url, downloading Items and Images to store in our DB.

Get some data:

    curl http://localhost:8000/api/v1/item/  # get all Items
    curl http://localhost:8000/api/v1/item/set/1;3/ # get a set of items
    curl http://localhost:8000/api/v1/item/1/ # get item with pk = 1
    curl http://localhost:8000/api/v1/item/?title__contains=Description # query with django filters

