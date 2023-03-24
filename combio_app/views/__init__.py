from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from elasticsearch_dsl.query import SimpleQueryString
from django.core.paginator import Paginator
from django.utils.functional import LazyObject
from pprint import pprint


from django.views import View
from ..models import Record
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


class ShowSearch(TemplateView):
    template_name = "combio_app/search.html"
    q = ""
    current_result = 0
    s_object = None

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        self.current_result = request.GET.get("result")
        s = RecordDocument.search().sort("id")
        self.q = request.GET.get("q", "")
        if self.q:
            # s = s.query('simple_query_string',query=self.q, fuzziness='AUTO')
            s = s.filter(SimpleQueryString(query=self.q, fields=["transcript"], default_operator="and"))
            s = s.highlight("transcript", number_of_fragments=0)
        self.es_query = s.to_dict()
        self.total_results = SearchResults(s)
        paginator = Paginator(self.total_results, 35)
        self.results = paginator.get_page(page)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = Record.objects.all()
        context["nbar"] = "search"
        context["q"] = self.q
        context["results"] = self.results
        if self.current_result:
            context["current_result"] = int(self.current_result)
        else:
            if self.results:
                context["current_result"] = self.results[0].id
        context["results_count"] = self.results.paginator.count
        return context
