from django.conf.urls import url

from . import views # import views so we can use them in urls.

urlpatterns = [
    url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
<<<<<<< HEAD
]
=======
    url(r'legalMentions', views.legalMentions, name="legalMentions"),
    url(r'contacts', views.contacts, name="contacts"),
    url(r'monCompte', views.monCompte, name="monCompte"),
    url(r'favoris', views.favoris, name="favoris"),
]


>>>>>>> us2
