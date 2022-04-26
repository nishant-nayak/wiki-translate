from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Project(models.Model):
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
