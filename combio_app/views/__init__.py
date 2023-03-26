from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import DetailView
from elasticsearch_dsl.query import SimpleQueryString
from django.core.paginator import Paginator
from django.utils.functional import LazyObject
from pprint import pprint
from jsonview.views import JsonView

import json
from django.core.serializers.json import DjangoJSONEncoder


from django.views import View
from ..models import Record, Collection
from ..documents import RecordDocument

from .errors import (
    ErrorView,
    Handle400View,
    Handle403View,
    Handle404View,
    Handle500View,
    HandleErrorView,
    handle500_view,
)

__all__ = [
    "ErrorView",
    "Handle400View",
    "Handle403View",
    "Handle404View",
    "Handle500View",
    "HandleErrorView",
    "handle500_view",
]


class LandingView(TemplateView):
    template_name = "combio_app/landing.html"

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nbar"] = "landing"
        return context


@method_decorator(login_required, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "combio_app/protected.html"


@method_decorator(login_required, name="dispatch")
class ShowRecords(TemplateView):
    template_name = "combio_app/records.html"

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = Record.objects.all()
        context["nbar"] = "records"
        return context


# https://djangotricks.blogspot.com/2018/06/data-filtering-in-a-django-website-using-elasticsearch.html
class SearchResults(LazyObject):
    def __init__(self, search_object):
        self._wrapped = search_object

    def __len__(self):
        return self._wrapped.count()

    def __getitem__(self, index):
        search_results = self._wrapped[index]
        if isinstance(index, slice):
            search_results = list(search_results)
        return search_results


@method_decorator(login_required, name="dispatch")
class ShowCollections(JsonView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collections = Collection.objects.all()
        context["collections"] = list(collections.values("pk", "name"))
        return context


@method_decorator(login_required, name="dispatch")
class Search(JsonView):
    q = ""
    c = []
    current_result = 0
    per_page = 20

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        per_page = request.GET.get("per_page")
        self.current_result = request.GET.get("result")
        s = RecordDocument.search().sort("id")
        self.q = request.GET.get("q", "")
        self.c = [eval(i) for i in request.GET.getlist("c[]", "")]
        s = s.filter("terms", collection__pk=self.c)
        if self.q:
            # s = s.query('simple_query_string',query=self.q, fuzziness='AUTO')
            s = s.filter(
                SimpleQueryString(
                    query=self.q,
                    fields=["transcript", "interviewers", "interviewees", "participants"],
                    default_operator="and",
                )
            )
            s = s.highlight("transcript", number_of_fragments=20, fragment_size=40)
            s = s.highlight("interviewers", number_of_fragments=0)
            s = s.highlight("interviewees", number_of_fragments=0)
            s = s.highlight("participants", number_of_fragments=0)
        self.es_query = s.to_dict()
        self.total_results = SearchResults(s)
        paginator = Paginator(self.total_results, per_page)
        self.results = paginator.get_page(page)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results_json = []
        for index, result in enumerate(self.results):
            clean_result = result.to_dict()
            del clean_result["transcript"]
            clean_result["meta"] = result.meta.to_dict()
            clean_result["index"] = index
            results_json.append(clean_result)
        context["results"] = results_json
        context["results_count"] = self.results.paginator.count
        return context


@method_decorator(login_required, name="dispatch")
class ShowSearch(TemplateView):
    template_name = "combio_app/search.html"

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nbar"] = "search"
        return context


@method_decorator(login_required, name="dispatch")
class ShowRecord(DetailView):
    model = Record

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
