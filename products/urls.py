from django.urls import path

from . import views as v # import views so we can use them in urls.

urlpatterns = [
    path(r'myBdd', v.myBddView.as_view(), name="index"), # "/store"
    path(r'myBdd/<int:actualize>', v.myBddView.as_view(), name="index"), # "/store"
    ]