from django.urls import path

from . import views as v # import views so we can use them in urls.


urlpatterns = [
    path(r'advancedSearch', v.AdvancedSearchView.as_view(), name="advancedSearch"),
]