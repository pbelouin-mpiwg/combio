# from django.db.models import JSONField
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
import json
import os
from pathlib import Path
from django_jsonform.models.fields import JSONField

BASE_DIR = Path(__file__).resolve().parent.parent

with open(
    os.path.join(BASE_DIR, "combio_app") + "/static/combio_app/json/combio_metadata_scheme.json", encoding="utf-8"
) as schema_file:
    metadata_schema = json.loads(schema_file.read())


def get_default_data():
    return {}


class Collection(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]


class Record(models.Model):
    metadata = JSONField(schema=metadata_schema)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.metadata["combio"]["title"]

    def title(self):
        return self.metadata["combio"]["title"]

    def transcript(self):
        return self.metadata["combio"]["transcript"]

    def interviewers(self):
        return [p["name"] for p in self.metadata["combio"]["participants"] if p["role"] == "interviewer"]

    def interviewees(self):
        return [p["name"] for p in self.metadata["combio"]["participants"] if p["role"] == "interviewee"]

    def participants(self):
        return [p["name"] for p in self.metadata["combio"]["participants"] if p["role"] == "participant"]

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
