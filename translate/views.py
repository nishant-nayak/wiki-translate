from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from wikipediaapi import Wikipedia
from pysbd import Segmenter

from .models import Project, Sentence, User

def index(request):
    '''
    Landing page view for the application.
    Accepts GET requests.
    '''
    return render(request, 'translate/index.html')

def register_user(request):
    '''
    View to register a single user.
    Accepts GET and POST requests.
    '''
    # Authenticated users need not register again
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    # If the request is a POST, create a new user
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

    # If the request is not a POST, render the register page
    return render(request, 'translate/register.html')

def login_user(request):
    '''
    Login Page view.
    Accepts GET and POST requests.
    '''
    # Authenticated users need not register again
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    # If the request is a POST, try to log the user in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # If the user is valid, log them in and redirect to the dashboard
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'translate/login.html', {
                "error": "Invalid username or password."
            }, status=400)

    # If the request is not a POST, render the login page
    return render(request, 'translate/login.html')

def logout_user(request):
    '''
    View to logout a user.
    Accepts GET requests.
    '''
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def input_title(request):
    '''
    View to input a title and target language for a new project.
    Accepts GET and POST requests.
    '''
    if request.method == "POST":
        # Get the title and target language from the form
        title = request.POST.get('article-title')
        lang = request.POST.get('target-lang')

        # Fetch the article summary from Wikipedia using the Wikipedia API
        summary = Wikipedia(language='en').page(title).summary

        # If the summary does not exist, return an error
        if len(summary) == 0:
            return render(request, 'translate/input-title.html', {
                'error': f'No summary found for the article: {title}.'
            }, status=400)

        # Segment the summary into sentences
        sentencesList = Segmenter(language='en', clean=False).segment(summary)

        # Create a new project with the given title and target language
        project = Project.objects.create(title=title, language=lang, creator=request.user)
        project.save()

        # Add the project to user's list of accessible projects
        request.user.accessible_projects.add(project)
        request.user.save()

        # Create a new sentence entry for each sentence in the summary
        for sentence in sentencesList:
            sen = Sentence.objects.create(project=project, original_sentence=sentence)
            sen.save()

        # Redirect to the annotate page for the new project
        return HttpResponseRedirect(reverse('annotate', args=(project.id,)))

    # If the request is not a POST, render the input_title page
    return render(request, 'translate/input-title.html', {
        "langs": Project.LANGUAGE_CHOICES
    })

@login_required
def annotate(request, pk):
    '''
    View to display the annotation interface for a project.
    Accepts GET and POST requests.
    '''
    if request.method == "POST":
        # Get the sentence ID and the new translation from the form
        for id in request.POST:
            if id != 'csrfmiddlewaretoken':
                sentence = Sentence.objects.get(id=id)
                sentence.translated_sentence = request.POST[id]
                sentence.save()

        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('dashboard'))

    # If the request is not a POST, render the annotate page
    project = Project.objects.get(id=pk)
    sentences = Sentence.objects.filter(project=project)

    return render(request, 'translate/annotate.html', {
            'sentences': sentences,
            'project': project,
            'target_lang': project.get_language_display()
        })

def dashboard(request):
    '''
    View to display the dashboard for a user.
    Accepts GET requests.
    '''
    projects = request.user.accessible_projects.all()
    return render(request, 'translate/dashboard.html', {
        'projects': projects
    })
