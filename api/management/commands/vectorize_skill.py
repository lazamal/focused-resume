from django.core.management.base import BaseCommand, CommandError
from api.models import Skill

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        pass