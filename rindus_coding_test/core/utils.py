import logging

from django.conf import settings
from django.db.models import QuerySet

from rindus_coding_test.core.adapters.comments import CommentInstanceAdapter
from rindus_coding_test.core.adapters.posts import PostInstanceAdapter
from rindus_coding_test.core.exceptions import CommentDoesNotExists, PostDoesNotExists
from rindus_coding_test.core.interfaces.interactions import InteractionsInterface
from rindus_coding_test.core.models import Comment, Post

logger = logging.getLogger(__name__)


def get_fake_api_client_by_version(api_version: str = "v1") -> InteractionsInterface:
    """
    Get adapter based on used api version
    :param api_version:
    :return: InteractionsInterface object
    """
    if api_version in settings.POST_COMMENT_ADAPTER_BY_VERSION.keys():
        full_module = settings.POST_COMMENT_ADAPTER_BY_VERSION[api_version]
        module, class_name = full_module.rsplit(".", 1)
        mod = __import__(module, fromlist=[class_name])
        klass = getattr(mod, class_name)
        fake_api_client = klass()
    else:
        # TODO: Out of scope - Fake api has just one version. This implementation is a 'just in case'
        raise NotImplementedError
    return fake_api_client


def load_initial_data() -> None:
    """Load initial data from remote service"""
    fake_api_client = get_fake_api_client_by_version()

    for post in fake_api_client.get_posts():
        Post.objects.create(**post.get_data_as_dict())

    for comment in fake_api_client.get_comments():
        Comment.objects.create(**comment.get_data_as_dict())


def update_local_data() -> None:
    """Update local data when found new data from remote sources.
    Following policy 'MASTER first' - It means MASTER data won't be modified if there is an existing instance
    """

    fake_api_client = get_fake_api_client_by_version()

    for post in fake_api_client.get_posts():
        try:
            Post.objects.get(id=post.id)
        except Post.DoesNotExist:
            Post.objects.create(**post.get_data_as_dict())
        else:
            # In this case we do nothing because MASTER (local) data is more relevant than API data.
            # If we had an update_datetime for the remote and local instances,
            # this could be taken into account to prioritize which data should be maintained.

            # This could be executed for data updating locally
            # Post.objects.filter(id=post.id).update(**post.get_data_as_dict())
            pass

    for comment in fake_api_client.get_comments():
        try:
            Comment.objects.get(id=comment.id)
        except Comment.DoesNotExist:
            Comment.objects.create(**comment.get_data_as_dict())
        else:
            # In this case we do nothing because MASTER (local) data is more relevant than API data.
            # If we had an update_datetime for the remote and local instances,
            # this could be taken into account to prioritize which data should be maintained.

            # This could be executed for data updating locally
            # Comment.objects.filter(id=comment.id).update(**comment.get_data_as_dict())
            pass


def update_remote_post_data(post_queryset: QuerySet):
    """Update Post remote data (fake api) with MASTER data"""
    fake_api_client = get_fake_api_client_by_version()
    for post_instance in post_queryset:
        post = PostInstanceAdapter(post_instance)
        try:
            fake_api_client.update_post(post)
        except PostDoesNotExists:
            fake_api_client.create_post(post)


def update_remote_comment_data(comment_queryset: QuerySet):
    """Update Comment remote data (fake api) with MASTER data"""
    fake_api_client = get_fake_api_client_by_version()
    for comment_instance in comment_queryset:
        comment = CommentInstanceAdapter(comment_instance)
        try:
            fake_api_client.update_comment(comment)
        except CommentDoesNotExists:
            fake_api_client.create_comment(comment)
