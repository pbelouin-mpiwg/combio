from django.db.models import JSONField
from django.db import models
from django.db.models import Count
from django.contrib.postgres.indexes import GinIndex
from django.contrib.auth.models import User
import django.contrib.postgres.search as pg_search


def get_default_data():
    return {}


class Collection(models.Model):
    name = models.CharField(max_length=512)
    metadata = JSONField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]


class Record(models.Model):
    record_index = models.IntegerField(blank=True)
    metadata = JSONField(null=True)
    transcript = models.TextField()
    sv = pg_search.SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["sv"])]
        ordering = ["pk"]

    def __str__(self):
        return self.metadata.combio.title

    metadata = JSONField(default=get_default_data)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
