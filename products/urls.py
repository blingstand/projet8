from django.urls import path
from . import views as v

urlpatterns = [
    path(r'infos', v.InfosView.as_view(), name="infos"),
    path(r'infos/<str:prod_name>', v.InfosView.as_view(), name="infos")
    ]
