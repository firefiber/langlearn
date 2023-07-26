from django.core.management.base import BaseCommand
from user_management.user_buffer import get_practice_buffer

class Command(BaseCommand):
    help = 'Tests the get_practice_buffer function'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username to test')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        practice_buffer = get_practice_buffer(username)

        self.stdout.write(self.style.SUCCESS('Practice Buffer:'))
        for word in practice_buffer:
            self.stdout.write(word)
