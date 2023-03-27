"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from jsonview.decorators import json_view

import combio_app.views

urlpatterns = [
    path("", include("combio_app.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("records/", combio_app.views.ShowRecords.as_view(), name="records"),
    path("create_record/", combio_app.views.CreateRecord.as_view(), name="create_record"),
    path("search/", combio_app.views.ShowSearch.as_view(), name="search"),
    path("help/", combio_app.views.ShowHelp.as_view(), name="help"),
    path("api/search/", json_view(combio_app.views.Search.as_view()), name="api_search"),
    path("api/collections/", json_view(combio_app.views.ShowCollections.as_view()), name="api_collections"),
    path("records/<int:pk>/", combio_app.views.ShowRecord.as_view(), name="show_record"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = combio_app.views.Handle400View.as_view()
handler403 = combio_app.views.Handle403View.as_view()
handler404 = combio_app.views.Handle404View.as_view()
handler500 = combio_app.views.handle500_view
