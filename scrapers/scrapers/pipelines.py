# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os
from asgiref.sync import sync_to_async
from jsonschema import validate
from pathlib import Path
import json
import coloredlogs, logging

coloredlogs.install(level="DEBUG")

BASE_DIR = Path(__file__).resolve().parent.parent

with open(
    os.path.join("/code/combio_app/static/combio_app/metadata_scheme/combio_metadata_scheme.json"),
    encoding="utf-8",
) as schema_file:
    metadata_schema = json.loads(schema_file.read())

sys.path.append("/code/")
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"

import django

django.setup()
from combio_app.models import Record, Collection

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ComBioScrapersPipeline(object):
    def open_spider(self, spider):
        self.file = open("welcometrust.json", "w")
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    @sync_to_async
    def process_item(self, item, spider):
        validate(instance=item, schema=metadata_schema)
        r = Record(metadata=item)
        col, success = Collection.objects.get_or_create(name=item["combio"]["collection"])
        r.collection = col
        r.save()
        return item


class ScrapersPipeline:
    def process_item(self, item, spider):
        print(item)
        return item
