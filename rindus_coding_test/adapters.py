import abc
from urllib.parse import urljoin

import requests

from rindus_coding_test.interfaces import InteractionsInterface


class PostInterface(abc.ABC):

    def __init__(self, raw_data) -> None:
        self.raw_data = raw_data

    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def user_id(self):
        pass

    @property
    @abc.abstractmethod
    def title(self):
        pass

    @property
    @abc.abstractmethod
    def body(self):
        pass

    def get_data_as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'body': self.body
        }


class PostJsonAdapter(PostInterface):

    @property
    def id(self):
        return self.raw_data['id']

    @property
    def user_id(self):
        return self.raw_data['userId']

    @property
    def title(self):
        return self.raw_data['title']

    @property
    def body(self):
        return self.raw_data['body']


class CommentInterface(abc.ABC):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def post_id(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def email(self):
        pass

    @property
    @abc.abstractmethod
    def body(self):
        pass

    def get_data_as_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'name': self.name,
            'email': self.email,
            'body': self.body
        }


class CommentJsonAdapter(CommentInterface):

    @property
    def id(self):
        return self.raw_data['id']

    @property
    def post_id(self):
        return self.raw_data['postId']

    @property
    def name(self):
        return self.raw_data['name']

    @property
    def email(self):
        return self.raw_data['email']

    @property
    def body(self):
        return self.raw_data['body']


class FakeApiAdapter(InteractionsInterface):
    base_url = 'https://jsonplaceholder.typicode.com/'

    def __init__(self, post_adapter=PostJsonAdapter, comment_adapter=CommentJsonAdapter):
        self.post_adapter = post_adapter
        self.comment_adapter = comment_adapter

    @staticmethod
    def _get_requests_method(method='get'):
        method = method.lower()
        request_method = getattr(requests, method, None)
        assert request_method is not None, f'Request method "{method}" not allowed'
        return request_method

    def _request(self, method='get', path=None, params=None, data=None):
        request_method = self._get_requests_method(method=method)
        url = urljoin(self.base_url, path)
        return request_method(url=url, params=params, data=data)

    def _parse_posts(self, raw_data):
        return [self.post_adapter(i) for i in raw_data]

    def get_posts(self):
        path = 'posts'
        response = self._request(path=path)
        data = response.json()
        return self._parse_posts(data)

    def _parse_comments(self, raw_data):
        return [self.comment_adapter(i) for i in raw_data]

    def get_comments(self):
        path = 'comments'
        response = self._request(path=path)
        data = response.json()
        return self._parse_comments(data)
