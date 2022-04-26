from django.shortcuts import render

from .models import Project

def index(request):
    return render(request, 'translate/input-title.html', {
        "langs": Project.LANGUAGE_CHOICES
    })
