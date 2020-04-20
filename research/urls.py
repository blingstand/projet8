""" this script manages the urls to give an appropriate http response"""
from django.urls import path

from . import views as v # import views so we can use them in urls.


urlpatterns = [
    # path(r'advancedSearch', v.AdvancedSearchView.as_view(), name="advancedSearch"),
    path(r'', v.IndexView.as_view(), name="index"),
    path(r'index', v.IndexView.as_view(), name="index"),
    path(r'results', v.ResultsView.as_view(), name="results"),
    path(r'123', v.titi.as_view(), name="titi"),
    path(r'results/<str:category>/<str:get_from_input>', v.ResultsView.as_view(), name="results"),
]
