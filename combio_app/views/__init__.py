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
    Record.objects.all().delete()
    i = 0
    while i < 50:
        r = Record(
            transcript="Cruisin' down the street in my '64 Jockin' the freaks, clockin' the dough Went to the park to get the scoop Knuckleheads out there cold-shootin' some hoops A car pulls up, who can it be?A fresh El Camino rollin', Kilo GHe rolls down his window and he started to say 'It's all about makin' that GTA'",
            metadata={
                "combio": {
                    "title": "Boyz-n-the-Hood",
                    "permalink": "https://www.youtube.com/watch?v=PWVNzYMyLTY",
                    "participants": [
                        {"name": "Pascal Belouin", "role": "interviewer"},
                        {"name": "Kim Pham", "role": "interviewee"},
                        {"name": "Michael Winter", "role": "interviewee"},
                        {"name": "Calvin Yeh", "role": "participant"},
                        {"name": "Hassan El Hajj", "role": "participant"},
                    ],
                }
            },
        )
        col = Collection.objects.all()[0]
        r.collection = col
        r.save()
        i = i + 1
    i = 0
    while i < 50:
        r = Record(
            transcript="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            metadata={
                "combio": {
                    "title": "Medical ethics education in Britain, 1963-1993 : the transcript of a Witness Seminar held by the Wellcome Trust Centre for the History of Medicine at UCL, London.",
                    "permalink": "https://www.youtube.com/watch?v=DsZOnZWpgNY",
                    "participants": [
                        {"name": "Pascal Belouin", "role": "interviewer"},
                        {"name": "Kim Pham", "role": "interviewee"},
                        {"name": "Michael Winter", "role": "interviewee"},
                        {"name": "Calvin Yeh", "role": "participant"},
                        {"name": "Hassan El Hajj", "role": "participant"},
                    ],
                }
            },
        )
        col = Collection.objects.all()[1]
        r.collection = col
        r.save()
        i = i + 1

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
