"""Test program that doing request to github server"""
import typing
import urllib.request
import urllib.error
import json
import unittest
from unittest import mock
import strawberry


@strawberry.type
class Lgn:
    """Class which implement name, repos"""
    name: typing.Optional[str]
    repos: typing.List[str]


def get_logins(login: str)-> Lgn:
    """Func for return inforamtion"""
    try:
        user_info_url = f"https://api.github.com/users/{login}"
        user_info_content = urllib.request.urlopen(user_info_url)
        user_info_content_read = user_info_content.read()
        name = json.loads(user_info_content_read)['name']
        repos_info_url= f"https://api.github.com/users/{login}/repos"
        repos_info_content = urllib.request.urlopen(repos_info_url)
        repos_info_content_read = repos_info_content.read()
        repos = [repo['name'] for repo in json.loads(repos_info_content_read)]
        return Lgn(
            name= name,
            repos= repos
        )
    except urllib.error.HTTPError as err:
        if err.code == 404:
            raise Exception("Can't find user") from err
        elif err.code == 403:
            raise Exception("Riched limit of request to the server") from err
        else:
            raise urllib.error.HTTPError from err


@strawberry.type
class Query:
    """Query"""
    @strawberry.field
    def logins(self, login: str)-> Lgn:
        return get_logins(login = login)


schema = strawberry.Schema(query=Query)


def mocked_requests_get(*args, **kwargs):
    """Fill information"""
    class MockResponse:
        """Fill information"""
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def read(self):
            """Fill information"""
            return json.dumps(self.json_data)

    if args[0] == 'https://api.github.com/users/test':
        return MockResponse({"name": "test"}, 200)
    elif args[0] == 'https://api.github.com/users/test/repos':
        return MockResponse([{"name": "repo1"}], 200)
    else:
        raise urllib.error.HTTPError(url= "",code=404, msg="", hdrs=None, fp=[])


class GetLoginTestCase(unittest.TestCase):
    """Fill information"""
    @mock.patch('urllib.request.urlopen', side_effect= mocked_requests_get)
    def test_fetch_existing_user(self, mock_get):
        """Fill information"""
        lgn = get_logins("test")
        self.assertEqual(lgn, Lgn("test", ["repo1"]))

    @mock.patch('urllib.request.urlopen', side_effect= mocked_requests_get)
    def test_fetch_not_existing_user(self, mock_get):
        """Fill information"""
        self.assertRaises(Exception, lambda: get_logins("test1"))


if __name__ == '__main__':
    unittest.main()
