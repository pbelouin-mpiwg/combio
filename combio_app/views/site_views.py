from http import HTTPStatus
from typing import Any

from django import http
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView
from ..models import Record


class ShowRecords(TemplateView):
    template_name = "combio_app/records.html"

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = Record.objects.all()
        context["nbar"] = "records"
        return context
