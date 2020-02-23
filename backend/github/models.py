import urllib.request, json
import re as re
from bs4 import BeautifulSoup
import argparse
import requests

from django.db import models

class Repo(models.Model):
    base_url = models.URLField(max_length=255)

    def __str__(self):
        return self.base_url

    # Find Number of Contributors
    def find_contributors(self):
        custom_url = self.base_url[18:]
        response = json.loads(requests.get('https://api.github.com/repos' + custom_url + '/contributors').text)

        num_contributors = len(response)

        # Create contributor object
        contributor = Contributor.objects.create(repo=self, number=num_contributors)
        contributor.save()

    # Find commits and commit dates
    def find_commits(self):
        commit_url = self.base_url + '/commits/master'
        commitpage = urllib.request.urlopen(commit_url)
        csoup = BeautifulSoup(commitpage, 'html.parser')
        while(True):
            dates = csoup.find_all(class_='commit-group-title')
            for d in dates:
                date = d.text.strip()[11:]
                msgs = d.find_next_sibling().find_all(class_='commit-title')
                for m in msgs:
                    msg = m.text.strip()

                    # Create commit object
                    commit = Commit.objects.create(repo=self, date=date, msg=msg)
                    commit.save()
            
            try:
                next_href = csoup.find(class_='btn btn-outline BtnGroup-item', text='Older').get('href')
                commit_url = next_href
                commitpage = urllib.request.urlopen(commit_url).read()
                csoup = BeautifulSoup(commitpage, 'html.parser')
            except:
                return

    def find_languages(self):
        langpage = urllib.request.urlopen(self.base_url)
        lsoup = BeautifulSoup(langpage, 'html.parser')

        languages = lsoup.find_all(class_='language-color', itemprop='keywords')
        for lang in languages:
            language = lang.get('aria-label')
            language = language.split()
            percent = language[1]
            language = language[0]

            # Create language object
            language = Language.objects.create(repo=self, name=language, percent=percent)
            language.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.find_contributors()
        self.find_commits()
        self.find_languages()

class Contributor(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

class Commit(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    msg = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

    def __str__(self):
        return self.msg

class Language(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    percent = models.CharField(max_length=255)

    def __str__(self):
        return self.name
