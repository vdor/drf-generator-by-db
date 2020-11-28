# drf-generator-by-db

The project can generate REST API based on your existing database.

**Note:**  After generation of an API you have to check out the code to remove secured fields, add permissions authorization and so and so forth

![drf-generator-by-db](https://github.com/vdor/drf-generator-by-db/raw/master/example.gif)

## Installation & Usage

- Clone repository

`git clone https://github.com/vdor/drf-generator-by-db.git`

- Create virtualenv and install dependencies

`cd drf-generator-by-db && virtualenv venv -p $(which python3.7) && source venv/bin/activate`

`pip install -r requirements.txt`


- Define the credentials of your database in `drf_generator/settings.py:77` into `DATABASES` variable


- Execute `python manage.py generate_rest`

Django could ask you to install additional dependencies. It depends on your database


- 🎉🎉🎉 REST API has been created (Run and check it out on the `/api` endpoint)


## TODO:
    - Autogenerate admin.py
    
    - Add Swagger
    
    - Autogenerate dummy permissions
    
    - Create new application with new version of API after each generation
 
 
 ### Aditional Info
 
 - Based on [inspectdb](https://github.com/django/django/blob/master/django/core/management/commands/inspectdb.py) of Django
