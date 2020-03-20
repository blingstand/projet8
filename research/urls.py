from django.urls import path

from . import views as v # import views so we can use them in urls.


urlpatterns = [
    path(r'advancedSearch', v.AdvancedSearchView.as_view(), name="advancedSearch"),
    path(r'results', v.ResultsView.as_view(), name="results"),
    path(r'', v.IndexView.as_view(), name="index"),
    path(r'index', v.IndexView.as_view(), name="index")


]