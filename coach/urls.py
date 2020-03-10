from django.urls import path

from . import views # import views so we can use them in urls.

urlpatterns = [
    path(r'', views.index, name="index"), # "/store" will call the method "index" in "views.py"
    path(r'index', views.index, name="index"),
    path(r'legalMentions', views.legalMentions, name="legalMentions"),
    path(r'contacts', views.contacts, name="contacts"),
    path(r'monCompte', views.monCompte, name="monCompte"),
    path(r'favoris', views.favoris, name="favoris"),
    path(r'logout', views.logoutUser, name="logout"),
    path(r'connection', views.connection, name="connection"),
    path(r'register', views.register, name="register"),

]


