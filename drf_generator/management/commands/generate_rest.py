from django.core.management.base import BaseCommand

from drf_generator.generator.generator import Generator


class Command(BaseCommand):
    help = 'Generates API for database'

    def handle(self, *args, **options):
        gen = Generator('api')
        gen.generate()
