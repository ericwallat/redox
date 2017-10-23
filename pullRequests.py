import requests
import sys
import re

GITHUB_API = 'https://api.github.com/'
TOKEN = str(sys.argv[1])


class github(object):
    def __init__(self, org):
        self.org = org
        self.pages = None

    def __str__(self):
        return str(self.org)

    def get_repos(self):
        url2 = GITHUB_API + 'orgs/' + str(self.org) + '/repos'
        repos = self.make_request(url2)
        return repos.json()

    def get_pulls(self, name, page):
        url2 = GITHUB_API + 'repos/' + self.org + '/' + name + '/pulls?state=all&per_page=100&page=' + str(page)
        print(url2)
        pulls = self.make_request(url2)
        return pulls.json()

    def make_request(self, url):
        response = requests.get(url, headers={'Authorization': 'token %s' % TOKEN})
        return response

    def get_pages(self, name):
        url2 = GITHUB_API + 'repos/' + self.org + '/' + name + '/pulls?state=all&per_page=100'
        pulls = self.make_request(url2)
        if pulls.links:
            return int(re.sub('.*?([0-9]*)$', r'\1', pulls.links['last']['url']))
        else:
            return 1

    def is_merged(self, pull):
        if pull['merged_at'] is None:
            return 0
        else:
            return 1


def main():

    g = github("lodash")
    pulls = []
    for repo in g.get_repos():
        pages = g.get_pages(repo['name'])
        for page in range(1, pages+1):
            pull = g.get_pulls(repo['name'], page)
            if pull:
                pulls.append(pull)
    pulls = [item for sublist in pulls for item in sublist]
    print(len(pulls))


if __name__ == '__main__':

    main()
