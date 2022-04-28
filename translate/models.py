'''
Models (Database Schema) for each entity is stored here.
The Django ORM uses this schema to create tables in the database
and perform CRUD operations on the database.
'''
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    User Model, stores information on all personnel
    '''
    pass

class Project(models.Model):
    '''
    Project Model, stores information on a single project
    '''
    LANGUAGE_CHOICES = [
        ('bn', 'Bengali'),
        ('gu', 'Gujarati'),
        ('hi', 'Hindi'),
        ('kn', 'Kannada'),
        ('ml', 'Malayalam'),
        ('mr', 'Marathi'),
        ('ne', 'Nepali'),
        ('or', 'Oriya'),
        ('pa', 'Punjabi'),
        ('si', 'Sinhala'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('ur', 'Urdu'),
    ]

    title = models.TextField(verbose_name="Wikipedia Article Title")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Project Creator")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name="Target Language")

class Sentence(models.Model):
    '''
    Sentence Model, stores information on a single sentence
    '''
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project")
    original_sentence = models.TextField(verbose_name="Original Sentence")
    translated_sentence = models.TextField(verbose_name="Translated Sentence", null=True, blank=True)
