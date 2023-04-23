# iot-devices-manager-api
Backend for my bachelor thesis - Local area network IoT devices management system. 

## Endpoints documentation

For Rest API documentation run the app and visit **http://127.0.0.1:8000/swagger/** .

## Installation

To get this project up and running locally on your computer follow the following steps.

Set up a python virtual environment.

Run the following command:
```
$ pip install -r requirements.txt
$ python manage.py makemigrations OR python manage.py makemigrations user_auth iot data_warehouse
$ python manage.py migrate
$ python manage.py runserver
```

Open a browser and go to http://localhost:8000/
