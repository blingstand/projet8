from django.conf.urls import url

from . import views # import views so we can use them in urls.

urlpatterns = [
    url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
    url(r'legalMentions', views.legalMentions),
    url(r'contacts', views.contacts),
]

# Salut erwan, 

# je fais face à un problème que je ne m'explique pas: 
# 	si je marque url(r'^contacts', views.contacts), > erreur 404
# 	mais si je marque url(r'contacts', views.contacts), > j'ai ma page
# 	=> c'est contraire à ce que j'ai dans le cours OC
# La surprise est que pour legalMentions c'est l'inverse: 
# 	si je marque url(r'^legalMentions', views.legalMentions), > j'ai ma page
# 	mais si je marque url(r'legalMentions', views.legalMentions), > erreur 404
# d'ù cela pourrait-il venir ?

