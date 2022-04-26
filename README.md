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
