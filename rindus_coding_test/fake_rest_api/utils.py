from django.core.exceptions import ValidationError

from rindus_coding_test.adapters import FakeApiAdapter
from rindus_coding_test.fake_rest_api.models import Post, Comment


def load_initial_data(api_version='v1'):
    if api_version == 'v1':
        fake_api_client = FakeApiAdapter()
    else:
        # TODO: Out of scope
        raise NotImplementedError

    for post in fake_api_client.get_posts():
        Post.objects.create(**post.get_data_as_dict())

    for comment in fake_api_client.get_comments():
        Comment.objects.create(**comment.get_data_as_dict())
