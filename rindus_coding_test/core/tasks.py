from collections.abc import Generator

from celery import shared_task
from django.db.models import QuerySet

from rindus_coding_test.core.models import Comment, Post
from rindus_coding_test.core.utils import (
    update_local_data,
    update_remote_comment_data,
    update_remote_post_data,
)


def batcherize_queryset(queryset: QuerySet, batch_size: int = 50) -> Generator:
    """
    Create ids batches from a queryset
    :param queryset: Original queryset that we want to split in batches
    :param batch_size: Size of the batches
    :return: Generator with batch size lists elements
    """
    ids = list(queryset.values_list("id", flat=True))

    for i in range(0, len(ids), batch_size):
        id_batch = ids[i : i + batch_size]  # noqa
        yield id_batch


@shared_task
def update_remote_post_data_task(post_ids: list[int]) -> None:
    update_remote_post_data(Post.objects.filter(id__in=post_ids))


@shared_task
def update_remote_comment_data_task(comment_ids: list[int]) -> None:
    update_remote_comment_data(Comment.objects.filter(id__in=comment_ids))


@shared_task
def sync_with_remote() -> None:
    """This method will sync local & remote data. To avoid long-term executions, querysets will be batchericed
    and classified in different celery executions (multiple workers)"""
    update_local_data()
    [
        update_remote_post_data_task.delay(ids)
        for ids in batcherize_queryset(queryset=Post.objects.all())
    ]
    [
        update_remote_comment_data_task.delay(ids)
        for ids in batcherize_queryset(queryset=Comment.objects.all())
    ]
