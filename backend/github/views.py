from django.shortcuts import render, redirect
from .models import Repo, Contributor, Commit, Language
from .forms import RepoForm
from django.http import JsonResponse, HttpResponse
from django.core import serializers

def home(request):
    if request.method == 'POST':
        form = RepoForm(request.POST)
        if form.is_valid():
            repo = form.save()
            return redirect('info', pk=repo.pk)
    else:
        form = RepoForm()
    return render(request, 'github/home.html', { 'form' : form })

def info(request, pk):
    repo = Repo.objects.get(pk=pk)
    contributors = repo.contributor_set.first()
    commits = repo.commit_set.all()
    languages = repo.language_set.all()
    return render(request, 'github/info.html')

def api(request, pk):
    repo = Repo.objects.get(pk=pk)
    r = serializers.serialize('json', [repo])
    contributors = serializers.serialize('json', [repo.contributor_set.first()])
    return HttpResponse(r)

def api_list(request, pk):
    repo = Repo.objects.get(pk=pk)
    commits = list(repo.commit_set.all().values())
    languages = list(repo.language_set.all().values())
    return JsonResponse({'commits' : commits, 'languages' : languages})
