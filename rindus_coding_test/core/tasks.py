from celery import shared_task

from rindus_coding_test.core.utils import update_local_data, update_remote_data


@shared_task
def sync_with_remote():
    update_local_data()
    update_remote_data()
