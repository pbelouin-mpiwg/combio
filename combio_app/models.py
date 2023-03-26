from django.db.models import JSONField
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


def get_default_data():
    return {}


class Collection(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]


class Record(models.Model):
    metadata = JSONField(null=True)

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

    metadata = JSONField(default=get_default_data)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
