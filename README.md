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

SECRET_KEY - project secret key. Required for local and production.

DEBUG - Set 'TRUE' for local development.

HOST_URL - Url host. Required to production.

DB_ENGINE - Type of database. Required to production.

DB_NAME - Database name. Required to production.


APP_API_ID - Telegram Client Api Id.

APP_API_HASH - Telegram Client Api Hash.

CAPTCHA_KEY - API key for anti-capthca.

## Create Client in Telegram
Instruction, how create new client in telegram [here](https://core.telegram.org/api/obtaining_api_id)


