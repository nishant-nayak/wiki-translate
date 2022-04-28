# WikiTranslate

A Django-based application that helps with translating Wikipedia articles from English to a variety of Indian Languages.

The application is deployed on Heroku, and is part of a CD pipeline using [GitHub Actions](https://github.com/nishant-nayak/wiki-translate/actions). The deployed site can be found at [https://wikitranslate-nishant.herokuapp.com/](https://wikitranslate-nishant.herokuapp.com/).

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

### Landing Page

Users are greeted with a landing page where they can register or login to the application.

![landing](/assets/landing.jpeg)

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

### Role Based Project Access

Normal users of the application do not have the option to create a new project. This feature is available only to the staff members of the application. The staff member allocation is handled by Django Groups. These staff members can then access the Django Admin Console to assign projects to certain users.

![role-based-access](/assets/role-based-access.png)

## Edge Case Handling

The following edge cases have been identified and handled:

1. Invalid Article Title
2. Duplicate Usernames
3. Password and Password confirmation fields not matching

## Remaining Work

The following work can still be done to improve the application

- Update the header navbar to include additional functionality
- Add a footer to include relevant links and sitemap
