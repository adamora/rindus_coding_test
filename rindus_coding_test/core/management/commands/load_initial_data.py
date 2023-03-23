import logging
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from rindus_coding_test.core.models import Comment, Post
from rindus_coding_test.core.utils import load_initial_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Load initial data in local (MASTER) from remote (Fake API)"""

    help = "Load initial data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--force", type=bool, default=False)

    def handle(self, *args: Any, **options: Any) -> str | None:
        # Check if data already loaded in database
        if options["force"]:
            Post.objects.all().delete()  # Comments will be deleted automatically by directive on_delete=models.CASCADE
        else:
            if Post.objects.exists() or Comment.objects.exists():
                raise CommandError(
                    "Data already loaded in database! "
                    'You can use "--force=True" argument to remove current database data'
                )

        load_initial_data()
        assert (
            Comment.objects.count() == 500 and Post.objects.count() == 100
        ), "Something wrong loading initial data!"
        logger.info("Data loaded successfully!")
