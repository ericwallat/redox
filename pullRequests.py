import requests
import sys

GITHUB_API = 'https://api.github.com/'
TOKEN = str(sys.argv[1])


class github(object):
    def __init__(self, org):
        self.org = org

    def __str__(self):
        return str(self.org)

    def get_repos(self):
        url2 = GITHUB_API + 'orgs/' + str(self.org) + '/repos'
        repos = self.make_request(url2)
        return repos.json()

    def get_pulls(self, name):
        url2 = GITHUB_API + 'repos/' + self.org + '/' + name + '/pulls'
        pulls = self.make_request(url2)
        return pulls.json()

    def get_merge(self, url):
        r = self.make_request(url)
        print(r.json())

    def make_request(self, url):
        response = requests.get(url, headers={'Authorization': 'token %s' % TOKEN})
        return response


def main():

    g = github("lodash")
    pulls = []
    for repo in g.get_repos():
        pull = g.get_pulls(repo['name'])
        if pull:
            pulls.append(pull)
    pulls = [item for sublist in pulls for item in sublist]
    for pull in pulls:
        g.get_merge(pull['url'])


if __name__ == '__main__':

    main()
