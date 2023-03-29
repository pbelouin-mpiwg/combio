from django.core.management.base import BaseCommand, CommandError
from combio_app.models import Record, Collection
import random
import pprint
import json
from .utils import create_record, purge_collections, purge_records, load_records

pp = pprint.PrettyPrinter(width=41, compact=True)


class Command(BaseCommand):
    help = "Loads dummy data"

    def handle(self, **options):
        purge_records()
        purge_collections()
        self.stdout.write(self.style.SUCCESS("Successfully purged records and collections"))
