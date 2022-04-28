from django.contrib import admin

from .models import *

# Register models on the Django Admin website
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Sentence)
