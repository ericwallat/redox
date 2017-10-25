import requests
import sys
import re

GITHUB_API = 'https://api.github.com/'
TOKEN = str(sys.argv[1])


class GitHub(object):
    """Base class for all objects returned by the API.

       Attributes:
           org (str): String representing the organization to be analyzed.

       """
    def __init__(self, org):
        self.org = org

    def __str__(self):
        return str(self.org)

    def get_repos(self):
        """Gets all the repos for the organization

        Returns:
            A json of all the repos for the organization

        """
        url2 = GITHUB_API + 'orgs/' + str(self.org) + '/repos'
        repos = self.make_request(url2)
        return repos.json()

    def get_pulls(self, name, page):
        """Gets all the pull requests for a specific repo and page

        Args:
            name: The name of the repo
            page: The page of the repo

        Returns:
            A json of the pull requests from a specific repo and page

        """
        url2 = GITHUB_API + 'repos/' + self.org + '/' + name + '/pulls?state=all&per_page=100&page=' + str(page)
        pulls = self.make_request(url2)
        return pulls.json()

    def make_request(self, url):
        """Sends the HTTP request to the Github API with the authorization header

        Args:
            url: The url to get data from

        Returns:
            A response object containing info about the API call

        """
        response = requests.get(url, headers={'Authorization': 'token %s' % TOKEN})
        return response

    def get_pages(self, name):
        """Gets the number of pages in a repo with 100 pull request per page

        Args:
            name: The name of the repo

        Returns:
            The number of pages if more than 1, otherwise returns 1

        """
        url2 = GITHUB_API + 'repos/' + self.org + '/' + name + '/pulls?state=all&per_page=100'
        pulls = self.make_request(url2)
        if pulls.links:
            return int(re.sub('.*?([0-9]*)$', r'\1', pulls.links['last']['url']))
        else:
            return 1

    def date_merged(self, pull):
        """Gets the number of pages in a repo with 100 pull request per page

        Args:
            pull: The pull request json

        Returns:
            The date the pull request was merged in format 'YYYY-MM-DDTHH:MM:SSZ'.
            0 if not merged

        """
        if pull['merged_at'] is None:
            return 0
        else:
            return pull['merged_at']


def main():

    g = GitHub('lodash')
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
