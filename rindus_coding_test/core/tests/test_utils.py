from unittest.mock import Mock, patch

import pytest

from rindus_coding_test.core.adapters.comments import CommentInstanceAdapter
from rindus_coding_test.core.adapters.posts import PostInstanceAdapter
from rindus_coding_test.core.interfaces.comments import CommentInterface
from rindus_coding_test.core.interfaces.interactions import InteractionsInterface
from rindus_coding_test.core.interfaces.posts import PostInterface
from rindus_coding_test.core.models import Comment, Post
from rindus_coding_test.core.tests.factories import CommentFactory, PostFactory
from rindus_coding_test.core.utils import (
    get_fake_api_client_by_version,
    load_initial_data,
    update_local_data,
)


def test_get_fake_api_client_by_version():
    client = get_fake_api_client_by_version(api_version="v1")
    assert isinstance(client, InteractionsInterface)


def test_get_fake_api_client_by_version_invalid_version():
    with pytest.raises(expected_exception=NotImplementedError):
        get_fake_api_client_by_version(api_version="INVALID")


def test_get_fake_api_client_by_version_invalid_setting(settings):
    settings.POST_COMMENT_ADAPTER_BY_VERSION["v1"] = "invalid.module.path"
    with pytest.raises(expected_exception=ModuleNotFoundError):
        get_fake_api_client_by_version(api_version="v1")


@pytest.mark.django_db
@patch("rindus_coding_test.core.utils.get_fake_api_client_by_version")
def test_load_initial_data(get_fake_api_client_by_version_mock):
    # Mocking endpoints to avoid calling external api
    mock_obj = Mock()
    built_post = PostFactory()
    post = PostInstanceAdapter(built_post)
    mock_obj.get_posts.return_value = [post]
    built_comment = CommentFactory(post=built_post)
    comment = CommentInstanceAdapter(built_comment)
    mock_obj.get_comments.return_value = [comment]
    get_fake_api_client_by_version_mock.return_value = mock_obj

    # Removed db objects to ensure no conflicts
    Post.objects.all().delete()
    Comment.objects.all().delete()

    # Calling tested method
    load_initial_data()

    assert Post.objects.count() == 1
    assert Comment.objects.count() == 1


class MockPostAdapter(PostInterface):
    @property
    def id(self):
        return self.raw_data["id"]

    @property
    def user_id(self):
        return self.raw_data["user_id"]

    @property
    def title(self):
        return self.raw_data["title"]

    @property
    def body(self):
        return self.raw_data["body"]


class MockCommentAdapter(CommentInterface):
    @property
    def id(self):
        return self.raw_data["id"]

    @property
    def post_id(self):
        return self.raw_data["post_id"]

    @property
    def name(self):
        return self.raw_data["name"]

    @property
    def email(self):
        return self.raw_data["email"]

    @property
    def body(self):
        return self.raw_data["body"]


@pytest.mark.django_db
@patch("rindus_coding_test.core.utils.get_fake_api_client_by_version")
def test_update_local_data(get_fake_api_client_by_version_mock):
    # Mocking endpoints to avoid calling external api
    mock_obj = Mock()
    updatable_post = PostFactory()
    mock_obj.get_posts.return_value = [
        PostInstanceAdapter(updatable_post),
        MockPostAdapter(
            {"id": 9999, "user_id": 99999942, "title": "test", "body": "test"}
        ),
    ]
    updatable_comment = CommentFactory(post=updatable_post)
    mock_obj.get_comments.return_value = [
        CommentInstanceAdapter(updatable_comment),
        MockCommentAdapter(
            {
                "id": 9999,
                "post_id": 9999,
                "name": "test",
                "email": "test@test.com",
                "body": "test",
            }
        ),
    ]
    get_fake_api_client_by_version_mock.return_value = mock_obj

    # Check db objects to ensure no conflicts
    assert Post.objects.count() == 1
    assert Comment.objects.count() == 1

    # Calling tested method
    update_local_data()

    assert Post.objects.count() == 2
    assert Comment.objects.count() == 2
