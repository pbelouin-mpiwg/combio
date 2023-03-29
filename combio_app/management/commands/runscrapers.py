from django.core.management.base import BaseCommand, CommandError
from combio_app.models import Record, Collection
import random
import pprint
import json
from .utils import create_record, purge_collections, purge_records, load_records
import subprocess
import signal
import os

pp = pprint.PrettyPrinter(width=41, compact=True)


class Command(BaseCommand):
    def handle(self, **options):
        purge_records()
        purge_collections()
        try:
            p = subprocess.Popen(["scrapy", "crawl", "queen_mary"], cwd="/code/scrapers/")
        except KeyboardInterrupt:
            p.send_signal(signal.SIGINT)
