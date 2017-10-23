import requests


class github(object):
    def __init__(self, org):
        self.org = org
        self.url = 'https://api.github.com/orgs/' + str(self.org)

    def __str__(self):
        return str(self.org)

    def get_repos(self):
        try:
            url2 = self.url + '/repos/'
            print url2
            request = Request(self.url + '/repos/')
            response = urlopen(request)
            repos = response.read()
            return repos
        except URLError, e:
            print 'Invalid organization. Error code:', e


if __name__ == '__main__':

    org = github("lodash")
    print org.get_repos()