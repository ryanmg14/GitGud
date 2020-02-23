import urllib.request
import re as re
from bs4 import BeautifulSoup
import argparse

class GitHubScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.num_contributors = 0
        self.commits = []

    # Find Number of Contributors
    def find_contributors(self):
        page = urllib.request.urlopen(self.base_url)
        soup = BeautifulSoup(page, 'html.parser')

        contributor = soup.find(class_='num text-emphasized')
        contributor_num = contributor.text
        self.num_contributors = contributor_num.strip()

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
                    commit = {}
                    commit['date'] = date
                    commit['msg'] = msg
                    self.commits.append(commit)
            
            try:
                next_href = csoup.find(class_='btn btn-outline BtnGroup-item', text='Older').get('href')
                commit_url = next_href
                commitpage = urllib.request.urlopen(commit_url).read()
                csoup = BeautifulSoup(commitpage, 'html.parser')
            except:
                return

    def parse_site(self):
        self.find_contributors()
        self.find_commits()

# Test Code
parser = argparse.ArgumentParser()
parser.add_argument('base_url')
args = parser.parse_args()
base_url = args.base_url

scraper = GitHubScraper(base_url)
scraper.parse_site()
print(scraper.num_contributors, scraper.commits)
