# WikiTranslate

A Django-based application that helps with translating Wikipedia articles from English to a variety of Indian Languages

## Installation Steps for Localhost Setup

```bash
pip install -r requirements.txt

mysql -u <username> -p
>> create database wikitranslate
>> exit

cd wikitranslate
cp 'example.env' .env
# fill up the .env file with your local info
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
# open localhost:8000 on your browser
```

## Features of the Application

### Login/Register functionality

Users who want to use the application can login/register through the web interface itself. Authentication is handled on the backend using Django's built-in authentication service.

![login-page](/assets/login.jpeg)

![register-page](/assets/register.jpeg)

### Projects Dashboard

The Projects dashboard gives an overview of all accessible projects to the current user, along with links to annotate those projects in the given language

![dashboard-empty](/assets/dashboard-empty.jpeg)

![dashboard-full](/assets/dashboard-full.jpeg)

### Creating and Annotating a new project

Users can enter the article title and target language from a given set of Indian languages. Once entered, the summary of the article is fetched from Wikipedia and a side-by-side annotation window is shown to the user. The user can annotate this article over multiple sessions (i.e. progress is saved each time the annotation is submitted).

![input-title](/assets/input-title.jpeg)

![annotate](/assets/annotate.jpeg)

## Remaining Work Todo

- Make the frontend UI for the annotation more user friendly with proper side-by-side translation boxes
- Creating role-based access for projects
