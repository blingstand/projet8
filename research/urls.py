from django.urls import path

from . import views as v # import views so we can use them in urls.


urlpatterns = [
    path(r'searchForm', v.SearchFormView.as_view(), name="searchForm"),
]