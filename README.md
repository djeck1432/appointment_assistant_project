# Appointment assistent project

There is a certain difficulty in applying for a visa in the United States. 
After registering the questionnaire on the consulate website and paying the state fee, 
the appointment calendar for the interview opens.
 
The problem is that the dates are constantly closed as if there are no free ones. 
But at one point, the Consulate opens them and the whole country tries to enroll.

Naturally, not everyone has time, but the service will help to do it.

## Build project and start coding

First of all, you must clone the repository and activate the virtual environment.

After, install the required dependencies:

```bash
$ pip install -r requirements.txt
```

Make a migrations:

```bash
$ python manage.py migrate
```

Run web server locally:

```bash
$ python manage.py runserver
```

Happy Coding!


## Environment variables


Some of the project settings are taken from environment variables.

There are variables available:

DJANGO_DEVELOPMENT_SERVER - Set to True when developing locally

```bash
$ export DJANGO_DEVELOPMENT_SERVER=True
```

SECRET_KEY - project secret key. Must be specified in production environment.
