import logging
from urllib.parse import urljoin

import requests
from rest_framework import status

from rindus_coding_test.core.exceptions import (
    CommentDoesNotExists,
    PostDoesNotExists,
    UnexpectedError,
)
from rindus_coding_test.core.interfaces.comments import CommentInterface
from rindus_coding_test.core.interfaces.interactions import InteractionsInterface
from rindus_coding_test.core.interfaces.posts import PostInterface
from rindus_coding_test.fake_rest_api.adapters.comments import CommentJsonAdapter
from rindus_coding_test.fake_rest_api.adapters.posts import PostJsonAdapter

logger = logging.getLogger(__name__)


class FakeApiAdapter(InteractionsInterface):
    base_url = "https://jsonplaceholder.typicode.com/"

    def __init__(
        self, post_adapter=PostJsonAdapter, comment_adapter=CommentJsonAdapter
    ):
        self.post_adapter = post_adapter
        self.comment_adapter = comment_adapter

    @staticmethod
    def _get_requests_method(method="get"):
        method = method.lower()
        request_method = getattr(requests, method, None)
        assert request_method is not None, f'Request method "{method}" not allowed'
        return request_method

    def _request(self, method="get", path=None, params=None, data=None):
        request_method = self._get_requests_method(method=method)
        url = urljoin(self.base_url, path)
        response = request_method(url=url, params=params, data=data)
        logger.info(
            f'Request send "{url}" - "{response.status_code}" - "{response.content}"',
            extra={
                "url": url,
                "params": params,
                "data": data,
                "response": response,
                "response_status_code": response.status_code,
                "response_content": response.content,
            },
        )
        return response

    def _parse_posts(self, raw_data):
        return [self.post_adapter(i) for i in raw_data]

    def get_posts(self):
        path = "posts"
        response = self._request(path=path)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self._parse_posts(data)

    def get_post(self, post_id: int):
        path = f"posts/{post_id}"
        response = self._request(path=path)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise PostDoesNotExists
        elif response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self.post_adapter(data)

    def create_post(self, post: PostInterface) -> PostInterface:
        path = "posts"
        payload = {
            "id": post.id,
            "userId": post.user_id,
            "title": post.title,
            "body": post.body,
        }
        response = self._request(method="POST", path=path, data=payload)
        if response.status_code != status.HTTP_201_CREATED:
            raise UnexpectedError
        data = response.json()
        return self.post_adapter(data)

    def update_post(self, post: PostInterface, partial=False) -> PostInterface:
        path = f"posts/{post.id}"
        payload = {
            "id": post.id,
            "userId": post.user_id,
            "title": post.title,
            "body": post.body,
        }
        response = self._request(
            method="PATCH" if partial else "PUT", path=path, data=payload
        )
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise PostDoesNotExists
        elif response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self.post_adapter(data)

    def _parse_comments(self, raw_data):
        return [self.comment_adapter(i) for i in raw_data]

    def get_comments(self):
        path = "comments"
        response = self._request(path=path)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self._parse_comments(data)

    def get_comment(self, comment_id: int):
        path = f"comments/{comment_id}"
        response = self._request(path=path)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise CommentDoesNotExists
        elif response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self.comment_adapter(data)

    def create_comment(self, comment: CommentInterface) -> CommentInterface:
        path = "comments"
        payload = {
            "id": comment.id,
            "postId": comment.post_id,
            "name": comment.name,
            "email": comment.email,
            "body": comment.body,
        }
        response = self._request(method="POST", path=path, data=payload)
        if response.status_code != status.HTTP_201_CREATED:
            raise UnexpectedError
        data = response.json()
        return self.comment_adapter(data)

    def update_comment(
        self, comment: CommentInterface, partial=False
    ) -> CommentInterface:
        path = f"comments/{comment.id}"
        payload = {
            "id": comment.id,
            "postId": comment.post_id,
            "name": comment.name,
            "email": comment.email,
            "body": comment.body,
        }
        response = self._request(
            method="PATCH" if partial else "PUT", path=path, data=payload
        )
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise CommentDoesNotExists
        elif response.status_code != status.HTTP_200_OK:
            raise UnexpectedError
        data = response.json()
        return self.comment_adapter(data)
