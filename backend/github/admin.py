from django.contrib import admin
from .models import Repo, Contributor, Commit, Language

admin.site.register(Repo)
admin.site.register(Contributor)
admin.site.register(Commit)
admin.site.register(Language)
