from django.core.management.base import BaseCommand, CommandError
from combio_app.models import Record, Collection
import random
import pprint
import json

pp = pprint.PrettyPrinter(width=41, compact=True)


def create_record(metadata):
    r = Record(metadata=metadata)
    col, success = Collection.objects.get_or_create(name=metadata["combio"]["collection"])
    r.collection = col
    r.save()


def purge_collections():
    Collection.objects.all().delete()


def purge_records():
    Record.objects.all().delete()


def load_records():
    f = open("./combio_app/management/commands/dummy_records.json")
    metadatas = json.load(f)
    col_names = ["SHI", "Wellcome Trust", "Queen Mary", "NIH"]
    i = 0
    while i < 1000:
        metadata = random.sample(metadatas, 1)[0]
        collection_name = random.sample(col_names, 1)[0]
        metadata["combio"]["collection"] = collection_name
        create_record(metadata)
        i = i + 1
