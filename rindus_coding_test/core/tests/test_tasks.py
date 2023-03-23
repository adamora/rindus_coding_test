import pytest

from rindus_coding_test.core.models import Post
from rindus_coding_test.core.tasks import batcherize_queryset
from rindus_coding_test.core.tests.factories import PostFactory


@pytest.mark.django_db
def test_batcherize_queryset():
    """A basic test to execute the batcherize_queryset method."""
    PostFactory.create_batch(100)
    batches = list(batcherize_queryset(queryset=Post.objects.all(), batch_size=50))
    assert len(batches) == 2
    assert len(batches[0]) == 50 and len(batches[1]) == 50
    assert set(batches[0] + batches[1]) == set(
        Post.objects.values_list("id", flat=True)
    )


# def test_user_count(settings):
#     """A basic test to execute the get_users_count Celery task."""
#     UserFactory.create_batch(3)
#     settings.CELERY_TASK_ALWAYS_EAGER = True
#     task_result = get_users_count.delay()
#     assert isinstance(task_result, EagerResult)
#     assert task_result.result == 3
