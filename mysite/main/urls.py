from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("WIG20", views.WIG20, name="WIG20"),
    path("chart/<id>/", views.chart, name="chart"),




]
