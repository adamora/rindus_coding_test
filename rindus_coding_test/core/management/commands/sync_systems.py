import logging
from typing import Any

from django.core.management.base import BaseCommand

from rindus_coding_test.core.tasks import sync_with_remote

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        sync_with_remote.delay()  # If sync_with_remote would receive params, those must be in json serializable format
