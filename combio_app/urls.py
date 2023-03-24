from django.urls import path

from combio_app import views

app_name = "combio_app"


urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("error/<int:code>", views.ErrorView.as_view(), name="error"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
]
