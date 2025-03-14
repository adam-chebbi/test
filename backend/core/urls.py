from django.urls import path, re_path
from core.views import GeneralListView, GeneralDetailView

urlpatterns = [
    re_path(r'^(?P<table>\w+)(?:\((?P<page>\d+)\))?/listview$', GeneralListView.as_view(), name='general-listview'),
    re_path(r'^(?P<table>\w+)\((?P<id>[-\w]+)\)/detail$', GeneralDetailView.as_view(), name='general-detail'),
]