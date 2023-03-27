from django.forms import ModelForm, Form
from django_jsonform.forms.fields import JSONFormField
from .models import Record
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(
    os.path.join(BASE_DIR, "combio_app") + "/static/combio_app/json/combio_metadata_scheme.json", encoding="utf-8"
) as schema_file:
    metadata_schema = json.loads(schema_file.read())


options = {"no_additional_properties": True}


class MetadataForm(Form):
    metadata = JSONFormField(schema=metadata_schema)
