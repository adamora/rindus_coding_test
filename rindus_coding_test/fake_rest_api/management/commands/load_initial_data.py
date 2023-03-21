import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser

from rindus_coding_test.fake_rest_api.models import Post, Comment
from rindus_coding_test.fake_rest_api.utils import load_initial_data

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Load initial data'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-f', '--force', type=bool, default=False)

    def handle(self, *args, **options):
        # Check if data already loaded in database
        if options['force']:
            Post.objects.all().delete()  # Comments will be deleted automatically by directive on_delete=models.CASCADE
        else:
            if Post.objects.exists() or Comment.objects.exists():
                raise CommandError('Data already loaded in database! '
                                   'You can use "--force=True" argument to remove current database data')

        load_initial_data()
        assert Comment.objects.count() == 500 and Post.objects.count() == 100, 'Something wrong loading initial data!'
        logger.info('Data loaded successfully!')
