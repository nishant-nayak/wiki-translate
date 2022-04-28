from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from wikipediaapi import Wikipedia
from pysbd import Segmenter

from .models import Project, Sentence, User

def index(request):
    return render(request, 'translate/login.html')

def input_title(request):
    if request.method == "POST":
        title = request.POST.get('article-title')
        lang = request.POST.get('target-lang')

        summary = Wikipedia(language='en').page(title).summary
        sentencesList = Segmenter(language='en', clean=False).segment(summary)

        project = Project.objects.create(title=title, language=lang, creator=request.user)
        project.save()

        for sentence in sentencesList:
            sen = Sentence.objects.create(project=project, original_sentence=sentence)
            sen.save()

        return HttpResponseRedirect(reverse('annotate', args=(project.id,)))

    return render(request, 'translate/input-title.html', {
        "langs": Project.LANGUAGE_CHOICES
    })

def register_user(request):
    '''
    View to register a single user. Accepts GET and POST requests.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        # Ensure password matches confirmation
        if password != request.POST["confirmation"]:
            return render(request, "translate/register.html", {
                "error": "Passwords must match."
            }, status=400)

        # Try to create a user with the given credentials
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        # If DB encounters an IntegrityError, return webpage with error message
        except IntegrityError:
            return render(request, 'translate/register.html', {
                'error': 'Username already exists!'
            }, status=400)

        # Log the user in
        login(request, user)
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'translate/register.html')

def login_user(request):
    '''
    Login Page view. Accepts GET and POST requests.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'translate/login.html', {
                "error": "Invalid username or password."
            }, status=400)

    return render(request, 'translate/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def annotate(request, pk):
    if request.method == "POST":
        for id in request.POST:
            if id != 'csrfmiddlewaretoken':
                sentence = Sentence.objects.get(id=id)
                sentence.translated_sentence = request.POST[id]
                sentence.save()

        return HttpResponseRedirect(reverse('dashboard'))

    project = Project.objects.get(id=pk)
    sentences = Sentence.objects.filter(project=project)

    return render(request, 'translate/annotate.html', {
            'sentences': sentences,
            'project': project,
            'target_lang': project.get_language_display()
        })

def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'translate/dashboard.html', {
        'projects': projects
    })
